from __future__ import print_function
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Adam Rojik

##### Imports
import threading
import cv2
import numpy as np
import pyrealsense2 as rs
import pyopenpose as op
import datetime as dt
import time
import math
import json

from rigid_transform_3D import rigid_transform_3D 

class datumFiller():
   def __init__(self):
      self.poseKeypoints = [np.array([])]


sharedIsrunningLock = threading.Condition()
sharedIsrunning = False

sharedVisionLock = threading.Condition()
sharedVision = {
   'zone': {
      'current': 4, # 3 - public, .. 0 - touch - updated in main
      'velocity': 0 # change from past record, will use only +1 - further, -1 - closer, but tracks even +-2 if fast change is detected
   },
   'distance': {
      'current': 7., # around max-detectable distance, should be in public zone
      'velocity': 0. # m/s - velocity from distance change, positive when getting further
   },
   'objects': {
      'nose': {
         'position': [0, 0, 0],
         'coords': [0, 0, 0],
         'current': False,
         'distance': 0
      },
      'closest': {
         'position': [0, 0, 0],
         'coords': [0, 0, 0],
         'current': False,
         'distance': 0
      }
   }
}



class videoConfig():
   def __init__(self):
      # Robot - camera calibration
      self.toRobRotation = np.eye(3)
      self.toRobTranslation = np.array([0, 0, 0])
      self.SCENE = 0

      # ROBOT
      self.ROBOT = {
         'vision': sharedVision,
         'touch': {
            'side': None
         }
      }

      self.ZONE = [0.45, 1.2, 3.7]
      self.motion = None
      self.skin = None
      self.isView = False
      self.isDebug = False
      self.isRecording = False
      self.exportName = ""
      self.startup = False
      self.startTime = time.time()
      
      

class videoPoseThread(threading.Thread):
   def __init__(self, configuration):
      """Private class for camera keypoint processing."""
      threading.Thread.__init__(self)
      self.config = configuration
      self.name = "videoPoseThread"
      
   def run(self):
      global sharedIsrunning, sharedIsrunningLock
      global sharedVision, sharedVisionLock
      
      # Load camera advanced settings
      ctx = rs.context()
      devices = ctx.query_devices()
      dev = devices[0]
      advnc_mode = rs.rs400_advanced_mode(dev)

      while not advnc_mode.is_enabled():
         print("Activating advanced mode")
         advnc_mode.toggle_advanced_mode(True)
         time.sleep(5)

      with open('cameraSettings.json', 'r') as json_file:
        as_json_object = json.load(json_file)

      # For Python 2, the values in 'as_json_object' dict need to be converted from unicode object to utf-8
      if type(next(iter(as_json_object))) != str:
         as_json_object = {k.encode('utf-8'): v.encode("utf-8") for k, v in as_json_object.items()}
      # The C++ JSON parser requires double-quotes for the json object so we need
      # to replace the single quote of the pythonic json to double-quotes
      json_string = str(as_json_object).replace("'", '\"')
      advnc_mode.load_json(json_string)

      #Create a config and configure the pipeline to stream
      # color and depth streams - should be kept same, otherwise projection won't work
      config = rs.config()
      config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)
      config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)

      # Define the codec and create VideoWriter object
      if self.config.isRecording:
         fourcc = cv2.VideoWriter_fourcc(*'x264')
         videoFPS = 15.
         videoTimer = self.config.startTime
         videoFrames = 0
         videoColored = cv2.VideoWriter(self.config.exportName + '.avi',fourcc, videoFPS, (1280,720))
         config.enable_record_to_file(self.config.exportName + '.bag')
         exportJoints = open(self.config.exportName + "_joints.py", 'w')
         exportJoints.write("times = []\n")
         exportJoints.write("names = []\n")
         exportJoints.write("keys = []\n")

         exportKeypoints = open(self.config.exportName + "_keypoints.py", 'w')
         exportKeypoints.write("times = []\n")
         exportKeypoints.write("keypoints3D = []\n")
         exportKeypoints.write("keypoints = []\n")

      # Create a pipeline
      pipeline = rs.pipeline()

      # Start streaming
      profile = pipeline.start(config)

      # Getting the depth sensor's depth scale (see rs-align example for explanation)
      depth_sensor = profile.get_device().first_depth_sensor()
      depth_scale = depth_sensor.get_depth_scale()

      # Create an align object
      # rs.align allows us to perform alignment of depth frames to others frames
      # The "align_to" is the stream type to which we plan to align depth frames.
      align_to = rs.stream.color
      align = rs.align(align_to)

      # Starting OpenPose
      opWrapper = op.WrapperPython()

      # Custom Params (refer to include/openpose/flags.hpp for more parameters)
      params = dict()
      params["model_folder"] = "/home/naolaptop/Software/openpose/models"
      params["net_resolution"] = "-1x144"
      params["number_people_max"] = 1
      params["tracking"] = 0

      opWrapper.configure(params)
      opWrapper.start()

      # Robot - camera calibration
      calibrationArm = 'LArm'

      tempMarkerZ = []
      tempMarkerPositions = []
      tempRobotPositions = []
      tempRobotTransformations = []

      markerPositions = []
      robotPositions = []
      robotTransformations = []
      closestObject = None

      robotOffset = {'ChestBoard/Button':np.array(self.config.motion.getPosition("ChestBoard/Button")[:3]), 'CameraTop': np.array(self.config.motion.getPosition("CameraTop")[:3])}
      nosePosition2D = [None, None]
      try:
         if self.config.startup:
            self.config.motion.doBlocking('calibration')
            self.config.motion.doBlocking('calibration0')
         elif self.config.isRecording:
            self.exportSetup(self.config.exportName, self.config.SCENE, self.config.toRobRotation, self.config.toRobTranslation)
            videoFrameTimer = time.time()

         sharedIsrunningLock.acquire()
         while sharedIsrunning:
            sharedIsrunningLock.release()
            # Get frameset of color and depth
            frames = pipeline.wait_for_frames()

            # Align the depth frame to color frame
            aligned_frames = align.process(frames)

            # Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame
            aligned_color_frame = aligned_frames.get_color_frame()

            # Validate that both frames are valid
            if not aligned_depth_frame or not aligned_color_frame:
               sharedIsrunningLock.acquire()
               continue

            # Intrinsics
            depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics

            # Get depth and color values in a np array
            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(aligned_color_frame.get_data())
      
            # Measure processing time
            timeP = dt.datetime.now()
      
            # Update robot offset to be aligned with current frame
            robotOffset = {'ChestBoard/Button':np.array(self.config.motion.getPosition("ChestBoard/Button", legCorrection=False)[:3]), 'CameraTop': np.array(self.config.motion.getPosition("CameraTop", legCorrection=False)[:3])}
            robotOffset2D = {}
            for part in robotOffset:
               robotOffset2D[part] = self.torso3DToPixel(depth_intrin, robotOffset[part], self.config.toRobRotation, self.config.toRobTranslation)
      
            if self.config.startup:
               # Calibration of camera position
               markers = cv2.aruco.detectMarkers(color_image, cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_50))
               marker3DCenter = np.array([0, 0, 0])
               for markerIndex in range(len(markers[0])):
                  marker = markers[0][markerIndex]
                  markerID = markers[1][markerIndex][0]
                  markerCenter = marker[0,:,:].sum(axis=0)*0.25
                  marker3DCenter = self.pixelTo3D(depth_intrin, depth_image, depth_scale, markerCenter[0], markerCenter[1])
            
               if marker3DCenter[2] > 0:
                  robotPosition = np.array(self.config.motion.getPosition(calibrationArm)[:3])
                  tempMarkerZ.append((marker3DCenter[2], len(tempMarkerPositions)))
                  tempMarkerPositions.append(marker3DCenter)
                  tempRobotPositions.append(robotPosition)
                  tempRobotTransformations.append(self.config.motion.getTransform(calibrationArm))
                  #print("tempCAM", marker3DCenter)
                  #print("tempROBOT", robotPosition)
            
                  if len(tempMarkerZ) > 1: # how many samples of each move
                     tempIndex = sorted(tempMarkerZ, key=lambda s:s[0])[len(tempMarkerZ)//2][1] # Get index of median
                     markerPositions.append(tempMarkerPositions[tempIndex])
                     robotTransformations.append(tempRobotTransformations[tempIndex])
                     robotPositions.append(tempRobotPositions[tempIndex])
                     print("CAM", markerPositions[-1])
                     print("ROBOT", robotPositions[-1])
               
                     tempMarkerZ = []
                     tempMarkerPositions = []
                     tempRobotPositions = []
                     tempRobotTransformations = []

               if len(markerPositions) < 7:
                  self.config.motion.doBlocking('calibration' + str(len(markerPositions)))
               else:
                  A = np.array(markerPositions)
                  B = np.array(robotPositions)
                  self.config.toRobRotation, self.config.toRobTranslation = rigid_transform_3D(A,B)
                  print("Calibration done: ", "\""+json.dumps([self.config.toRobRotation.tolist(), self.config.toRobTranslation.tolist()])+"\"")
                  self.config.motion.doBlocking('Stand')
                  self.config.startup = False
                  if self.config.isRecording:
                     self.exportSetup(self.config.exportName, self.config.SCENE, self.config.toRobRotation, self.config.toRobTranslation)
                     videoFrameTimer = time.time()
                     
                  sharedIsrunningLock.acquire()
                  continue
            else:
               visibleObjects = {}
               closestObject = None
               self.config.ROBOT['vision']['objects']['nose']['current'] = False

               # Process Image
               keypoints3DPrint = {}
               datum = op.Datum()
               imageToProcess = color_image
               for part in robotOffset:
                  if not math.isnan(robotOffset2D[part][0]):
                     rob2DTuple = self.toTupleInt(robotOffset2D[part])
                     cv2.circle(imageToProcess, rob2DTuple, 10, (0,0,0), 10)
               datum.cvInputData = imageToProcess
               opWrapper.emplaceAndPop([datum])

               # Keypoints detection
               distances = []
               if datum.poseKeypoints.size > 1:
                  keypoints3D = self.keypointsTo3D(depth_intrin, depth_image, depth_scale, datum.poseKeypoints[0], filtered=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 23, 24, 25], area=5)
                  for keypointIndex in keypoints3D.keys():
                     # Closest object detection
                     keypoint3D = keypoints3D[keypointIndex]
                     keypoints3DPrint[keypointIndex] = keypoints3D[keypointIndex].tolist()
                     keypoint2D = datum.poseKeypoints[0][keypointIndex]
                     coords = np.dot(self.config.toRobRotation, keypoint3D) + self.config.toRobTranslation

                     partDistances = {}
                     distance = (None, float('inf'))
                     for part in robotOffset:
                        partDistances[part] = np.linalg.norm(coords - robotOffset[part])
                        if partDistances[part] < distance[1]:
                           distance = (part, partDistances[part])

                     if keypoint3D[2] > 0:
                        visibleObjects[keypointIndex] = {
                           'position': keypoint2D,
                           'coords': coords,
                           'coordsOrigin': keypoint3D,
                           'distance': distance[1],
                           'distanceKey': distance[0],
                           'partDistances': partDistances
                        }
                        distances.append(distance[1])
                        if closestObject == None or distance[1] < visibleObjects[closestObject]['distance']:
                           closestObject = keypointIndex
               else:
                  datum = datumFiller()

               if len(distances) < 3 or np.var(distances, ddof=1) > 0.1:
                  closestObject = None
            
               if not closestObject is None:
                  # Measurements
                  distance = visibleObjects[closestObject]['distance']

                  noseKeypoint = filter(lambda x: x in visibleObjects.keys(), [0,16,15,18,17])
                  if len(noseKeypoint) > 0:
                     noseKeypoint = noseKeypoint[0]
                     noseCopy = dict(visibleObjects[noseKeypoint])
                     noseCopy['current'] = True
                     self.config.ROBOT['vision']['objects']['nose'] = noseCopy

                     #z = visibleObjects[noseKeypoint]['coordsOrigin'][2]
                     #if abs(visibleObjects[noseKeypoint]['distance'] - visibleObjects[closestObject]['distance']) > 0.3:
                     #   z = visibleObjects[closestObject]['coordsOrigin'][2]

                     #nose3D = np.array(rs.rs2_deproject_pixel_to_point(depth_intrin, [float(visibleObjects[noseKeypoint]['position'][0]), float(visibleObjects[noseKeypoint]['position'][1])], z))
                     #coords = np.dot(self.config.toRobRotation, nose3D) + self.config.toRobTranslation - robotOffset['CameraTop']
                     #if (noseDistance < 1.5 and noseKeypoint == 0) or noseDistance > 1.5:
                     #   visibleObjects[noseKeypoint]['distance'] = noseDistance
                     #   visibleObjects[noseKeypoint]['distanceKey'] = 'CameraTop'

                  processingTime = dt.datetime.now() - timeP
                  self.config.ROBOT['vision']['distance']['velocity'] = (distance - self.config.ROBOT['vision']['distance']['current'])/processingTime.total_seconds()
                  self.config.ROBOT['vision']['distance']['current'] = distance
      
                  updated = False
                  for i in range(len(self.config.ZONE)):
                     if distance <= self.config.ZONE[i]:
                        self.config.ROBOT['vision']['zone']['velocity'] = i + 1 - self.config.ROBOT['vision']['zone']['current']
                        self.config.ROBOT['vision']['zone']['current'] = i + 1
                        updated = True
                        break
                  if not updated:
                     self.config.ROBOT['vision']['zone']['velocity'] = 4 - self.config.ROBOT['vision']['zone']['current']
                     self.config.ROBOT['vision']['zone']['current'] = 4
               else:
                  self.config.ROBOT['vision']['zone']['velocity'] = 0

               self.config.ROBOT['touch']['side'] = self.config.skin.whichSide(True)
               if self.config.ROBOT['touch']['side'] != None:
                  self.config.ROBOT['vision']['zone']['current'] = 0

               sharedVisionLock.acquire()
               sharedVision = dict(self.config.ROBOT['vision'])
               sharedVisionLock.release()


            # Processing time
            processingTime = dt.datetime.now() - timeP
            if self.config.isDebug:
               print(str(round((time.time() - videoTimer)/60., 2)) + " min " + str(round(1/processingTime.total_seconds(), 2))+ " FPS") # Frame-rate
      
            # Prepare image to be used by opencv in order to show it on the screen
            # mostly used for testing/debug, we will probably need to remove this in actual scripts
            # to improve performance.
            if self.config.isView or self.config.isRecording:
               depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
               depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
               try:
                  images = datum.cvOutputData#np.hstack((datum.cvOutputData, depth_colormap))
               except:
                  images = color_image#np.hstack((color_image, depth_colormap

               if self.config.isView:
                  cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)

               if images is not None:
                  if self.config.ROBOT['vision']['zone']['current'] <= 3 and self.config.ROBOT['vision']['zone']['current'] > 0 and (self.config.ROBOT['vision']['objects']['nose']['current'] or nosePosition2D[0] != None):
                     if self.config.ROBOT['vision']['objects']['nose']['current']:
                        nosePosition2D = self.config.ROBOT['vision']['objects']['nose']['position']
                     nose2DTuple = self.toTupleInt(nosePosition2D)
                     rob2DTuple = self.toTupleInt(robotOffset2D['CameraTop'])
                     cv2.arrowedLine(images, rob2DTuple, nose2DTuple, (0, 255, 0), int(10*self.config.ROBOT['vision']['objects']['nose']['partDistances']['CameraTop'])+1, tipLength = 0.01+0.05*self.config.ROBOT['vision']['objects']['nose']['partDistances']['CameraTop'])

                     text = "|"+str(round(self.config.ROBOT['vision']['objects']['nose']['partDistances']['CameraTop'],2))+"| m"
                     cv2.putText(images, text, nose2DTuple, cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,0), 5)
                     cv2.putText(images, text, nose2DTuple, cv2.FONT_HERSHEY_DUPLEX, 2, (255,255,255), 4)
                     nose2DTuple = (nose2DTuple[0], nose2DTuple[1] + 35)
            
                     text = str(map(round, self.config.ROBOT['vision']['objects']['nose']['coords'], len(self.config.ROBOT['vision']['objects']['nose']['coords'])*[2]))
                     cv2.putText(images, text, nose2DTuple, cv2.FONT_HERSHEY_DUPLEX, 1.1, (0,0,0), 3)
                     cv2.putText(images, text, nose2DTuple, cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)

                  if closestObject != None:
                     closestPosition2D = visibleObjects[closestObject]['position']
                     closest2DTuple = self.toTupleInt(closestPosition2D)
                     rob2DTuple = self.toTupleInt(robotOffset2D[visibleObjects[closestObject]['distanceKey']])
                     cv2.circle(images, closest2DTuple, 10, (0,0,255), 10)
                     cv2.arrowedLine(images, rob2DTuple, closest2DTuple, (255, 0, 0), 5, tipLength = 0.05)

                     text = "|"+str(round(visibleObjects[closestObject]['distance'],2))+"| m"
                     cv2.putText(images, text, closest2DTuple, cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,0), 5)
                     cv2.putText(images, text, closest2DTuple, cv2.FONT_HERSHEY_DUPLEX, 2, (255,255,255), 4)
                     closest2DTuple = (closest2DTuple[0], closest2DTuple[1] + 35)
            
                     text = str(map(round,visibleObjects[closestObject]['coords'], len(visibleObjects[closestObject]['coords'])*[2]))
                     cv2.putText(images, text, closest2DTuple, cv2.FONT_HERSHEY_DUPLEX, 1.1, (0,0,0), 3)
                     cv2.putText(images, text, closest2DTuple, cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)
            
                  text = "Action: " + str(self.config.motion.lastMove())
                  cv2.putText(images,text, (10,35), cv2.FONT_HERSHEY_DUPLEX, 1.1, (0,0,0), 3)
                  cv2.putText(images,text, (10,35), cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)

                  text = "Zone: " + str(self.config.ROBOT['vision']['zone']['current'])
                  cv2.putText(images,text, (10,75), cv2.FONT_HERSHEY_DUPLEX, 1.1, (0,0,0), 3)
                  cv2.putText(images,text, (10,75), cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)
            
                  text = "Touch: " + str(self.config.ROBOT['touch']['side']) # touch is no longer avalaible here
                  cv2.putText(images,text, (10,115), cv2.FONT_HERSHEY_DUPLEX, 1.1, (0,0,0), 3)
                  cv2.putText(images,text, (10,115), cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)
            

                  text = dt.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
                  cv2.putText(images,text, (10,700), cv2.FONT_HERSHEY_DUPLEX, 1.1, (0,0,0), 3)
                  cv2.putText(images,text, (10,700), cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)

                  if self.config.isRecording and not self.config.startup:
                     timer = time.time() - videoTimer
                     while videoFrames < timer*videoFPS:
                        # Export keypoints
                        exportKeypoints.write("times.append(" + str(timer)+ ")\n")
                        exportKeypoints.write("keypoints3D.append(" + str(keypoints3DPrint)+ ")\n")
                  
                        exportKeypoints.write("keypoints.append(" + str(datum.poseKeypoints[0].tolist())+ ")\n")
                  
                        videoColored.write(images)
                        videoFrames += 1
                        timer = time.time() - videoTimer

                     # Export robot angles
                     bodyJoints = self.config.motion.getBodyNames("Body")
                     exportJoints.write("times.append(" + str(timer)+ ")\n")
                     exportJoints.write("names.append(" + str(bodyJoints)+ ")\n")
                     exportJoints.write("keys.append(" + str(self.config.motion.getAngles("Body"))+ ")\n")

                  if self.config.isView:
                     cv2.imshow('RealSense', images)
      
            key = cv2.waitKey(1)
            # Press esc or 'q' to close the image window
            if key & 0xFF == ord('q') or key == 27:
               break
               
            sharedIsrunningLock.acquire()
      finally:
         if self.config.isRecording:
            videoColored.release()
            exportJoints.close()
            exportKeypoints.close()
      
         if self.config.isView:
            cv2.destroyAllWindows()
         # Stop streaming
         pipeline.stop()
         sharedIsrunningLock.acquire()
         sharedIsrunning = False
         sharedIsrunningLock.release()
         print("Qutting video.")
     
   def toTupleInt(self, x):
      return (int(x[0]), int(x[1]))
            
   def pixelTo3D(self, depth_intrin, depth_image, depth_scale, x, y, area=0):
      if x < 0 or y < 0:
         return np.array([0, 0, 0])
   
      updatedX = min(depth_image.shape[1] - 1, int(math.floor(x)))
      updatedY = min(depth_image.shape[0] - 1, int(math.floor(y)))
      z = depth_image[max((updatedY - area), 0):min((updatedY + area + 1), depth_image.shape[0]), max((updatedX-area),0):min((updatedX+area+1), depth_image.shape[1])].min() * depth_scale
      return np.array(rs.rs2_deproject_pixel_to_point(depth_intrin, [float(x), float(y)], z))

   def torso3DToPixel(self, depth_intrin, position, toRobRotation = np.eye(3), toRobTranslation = np.array([0, 0, 0])):
      position = np.dot(np.linalg.inv(toRobRotation), (position - toRobTranslation))
      return rs.rs2_project_point_to_pixel(depth_intrin, position.tolist())

   def exportSetup(self, exportName, SCENE, toRobRotation, toRobTranslation):
      with open(exportName + "_setup.txt", 'w') as file:
         file.write("-s "+str(SCENE)+" -c \""+json.dumps([toRobRotation.tolist(), toRobTranslation.tolist()])+"\"")
         file.close()

   def keypointsTo3D(self, depth_intrin, depth_image, depth_scale, keypoints, filtered, area=0):
      """Returns most probable 3D positions of 2D keypoints. Z taken from depth_image for each keypoint from index argmin|KeypointDepthArea - areaWeightedAvgDepthAroundAllKeypoints|.
         :keypoints are points from openpose
         :filtered are keypoint IDs to be ignored
         :area around keypoints to be selected from"""
      keypointAreas = {}
      resultKeypoints = {}
      kAverages = []
      kWeights = []
      for keypointIndex in filter(lambda x: x not in filtered, range(len(keypoints))):
         keypoint = keypoints[keypointIndex]
         if keypoint[2] > 0.2: # detection limit
            x = keypoint[0]
            y = keypoint[1]
         
            if x < 0 or y < 0:
               continue
      
            updatedX = min(depth_image.shape[1] - 1, int(math.floor(x)))
            updatedY = min(depth_image.shape[0] - 1, int(math.floor(y)))
            keypointAreas[keypointIndex] = {}
            keypointAreas[keypointIndex]['coords'] = [max((updatedY - area), 0), min((updatedY + area + 1), depth_image.shape[0]), max((updatedX-area),0), min((updatedX+area+1), depth_image.shape[1])]
            keypointAreas[keypointIndex]['area'] = depth_image[keypointAreas[keypointIndex]['coords'][0]:keypointAreas[keypointIndex]['coords'][1], keypointAreas[keypointIndex]['coords'][2]:keypointAreas[keypointIndex]['coords'][3]] * depth_scale
            keypointAreas[keypointIndex]['avg'] = np.average(keypointAreas[keypointIndex]['area'])
            keypointAreas[keypointIndex]['size'] = (keypointAreas[keypointIndex]['coords'][1] - keypointAreas[keypointIndex]['coords'][0]) * (keypointAreas[keypointIndex]['coords'][3] - keypointAreas[keypointIndex]['coords'][2])

            kAverages.append(keypointAreas[keypointIndex]['avg'])
            kWeights.append(keypointAreas[keypointIndex]['size'])

      try:
         bodyAverage = np.average(kAverages, weights=kWeights)
         for keypointIndex in keypointAreas.keys():
            keypoint = keypointAreas[keypointIndex]
            zIndexes = np.argmin(np.abs(keypoint['area'] - bodyAverage))
            z = keypoint['area'].flatten()[zIndexes]
            if z > 0:
               resultKeypoints[keypointIndex] = np.array(rs.rs2_deproject_pixel_to_point(depth_intrin, [float(keypoints[keypointIndex][0]), float(keypoints[keypointIndex][1])], z))   
      except:
         return {}
      return resultKeypoints



class start():
   def __init__(self, configuration):
      """Starts separate thread for camera processing."""
      global sharedIsrunning
      self.config = configuration
      if self.config.motion == None:
         self.config.startup = False

      sharedIsrunning = True
      videoPoseThread(self.config).start()

   def isRunning(self):
      global sharedIsrunning, sharedIsrunningLock
      sharedIsrunningLock.acquire()
      isStartup = self.config.startup
      running = sharedIsrunning
      sharedIsrunningLock.release()
      while running and isStartup:
         time.sleep(.5)
         sharedIsrunningLock.acquire()
         isStartup = self.config.startup
         running = sharedIsrunning
         sharedIsrunningLock.release()
      return running

   def getVision(self):
      global sharedVision, sharedVisionLock
      localVision = None
      sharedVisionLock.acquire()
      localVision = dict(sharedVision)
      sharedVisionLock.release()
      return localVision

   def stop(self):
      global sharedIsrunning, sharedIsrunningLock
      sharedIsrunningLock.acquire()
      sharedIsrunning = False
      sharedIsrunningLock.release()
      time.sleep(1)
      print("Exit video.")
