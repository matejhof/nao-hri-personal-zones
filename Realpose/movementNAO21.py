#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Adam Rojik

##### Imports
import threading
import numpy as np
import math
import time
from naoqi import ALProxy

import movementNAO21DB as mvdb
from safeMotion import safeMotion

class config:
   def __init__(self):
      """Configuration object. isDebug can be turned on by setting config.isDebug = True."""
      self.motion = None
      self.posture = None
      self.isDebug = False
      self.isRecording = False
      self.exportName = ""
      self.safeMotion = None
      self.startTime = time.time()

   def setupSafeMotion(self, ip, port, jointLimits="limits/checkedSafe.csv", headLimits="limits/headSafe.csv", currentLimits="limits/currentMax.csv", safePositions=None):
      """See safeMotion module for details."""
      self.safeMotion = safeMotion(ip, port, jointLimits, headLimits, currentLimits, safePositions)

   def connect(self, ip, port):
      """Connect to NAO with given IP and PORT. False if some error occured during connection."""
      try:
         self.motion = ALProxy("ALMotion", ip, port)
         self.posture = ALProxy("ALRobotPosture", ip, port)
         self.memory = ALProxy("ALMemory", ip, port)
         return True
      except:
         self.motion = None
         self.posture = None
      return False



lockDo = threading.Condition()
sharedDo = None

lockTimeout = threading.Condition()
sharedTimeout = 0

lockDone = threading.Condition()
sharedDone = None

sharedLLeg = 0

lockLookat = threading.Condition()
sharedLookat = None

lockIsrunning = threading.Condition()
sharedIsrunning = False

class headtrackingThread(threading.Thread):
   def __init__(self, configuration):
      """Private class used for controlling NAOs head in separate thread."""
      threading.Thread.__init__(self)
      self.config = configuration
      self.name = "headtrackingThread"
      
   def run(self):
      global lockTimeout, sharedTimeout
      global lockDone, sharedDone
      global lockLookat, sharedLookat
      global lockIsrunning, sharedIsrunning
      global sharedLLeg # does not need lock, changed only on startup

      lockIsrunning.acquire()
      while sharedIsrunning:
         lockIsrunning.release()

         lockLookat.acquire()
         localLookat = sharedLookat
         sharedLookat = None
         lockLookat.release()
         
         lockTimeout.acquire()
         timeout = sharedTimeout - time.time()
         lockTimeout.release()

         lockDone.acquire()
         localDone = sharedDone
         lockDone.release()

         # Get transformation from torso to head (only Z is non-0 and without rotation)
         torsoToHead = self.config.motion.getPosition("Head", 0, True)[2] + 0.03 # getPosition returns quaternion format
         
         # When moving, load its sequence into movement, so lookAt knows whether it can be used
         movement = {'names':[]}
         if localDone != None:
            mvdata = mvdb.get(localDone)
            if mvdata:
               movement = mvdata

         # determine look-at angles
         if not localLookat is None and ((not "HeadYaw" in movement["names"] and not "HeadPitch" in movement["names"]) or timeout < 0):
            localLookat[2] -= torsoToHead # Now at head position
            yawGoal = math.atan2(localLookat[1], localLookat[0])
            pitchGoal = -math.atan2(localLookat[2], localLookat[0])
            
            # From-leg calibration
            pitchGoal += self.config.memory.getData("Device/SubDeviceList/LHipPitch/Position/Sensor/Value") - sharedLLeg
         
            # change look-at so it is within eligible limits, yaw is more important (left-right)
            limitsYaw = self.config.safeMotion.jointLimits["HeadYaw"]
            limitedYawGoal = np.clip(yawGoal, limitsYaw[0], limitsYaw[1])
            limitedYawGoal = np.clip(limitedYawGoal, -0.5078, 0.5078)
            try:
               limitsPitch = self.config.safeMotion.headPitchLimitsAtYaw(limitedYawGoal)
               limitedPitchGoal = np.clip(pitchGoal, limitsPitch[0], limitsPitch[1])
               
               #if self.config.isDebug:
               #   print("Looking at: ", limitedYawGoal, limitedPitchGoal, localDone)
                  
               angles = self.config.motion.getAngles(["HeadYaw", "HeadPitch"], True)
               a = limitedYawGoal - angles[0]
               b = limitedPitchGoal - angles[1]
               
               lockDone.acquire()
               if localDone != sharedDone:   
                  lockDone.release()               
                  lockIsrunning.acquire()
                  continue
               lockDone.release()               

               self.config.motion.setAngles(["HeadYaw", "HeadPitch"], [limitedYawGoal, limitedPitchGoal], math.sqrt(a**2+b**2)*0.2) # non-blocking
            except NameError: # Yaw not within limits, should never occur, because clip
               lockIsrunning.acquire()
               continue
         
         time.sleep(0.02)
         lockIsrunning.acquire()
      lockIsrunning.release()
      print("Quitting movement HEAD.")



class movementThread(threading.Thread):
   def __init__(self, configuration):
      """Private class used for controlling NAOs movement in separate thread."""
      threading.Thread.__init__(self)
      self.config = configuration
      self.name = "movementThread"

   def run(self):
      global lockTimeout, sharedTimeout
      global lockDo, sharedDo
      global lockDone, sharedDone
      global lockLookat, sharedLookat
      global lockIsrunning, sharedIsrunning

      lockIsrunning.acquire()
      while sharedIsrunning:
         lockIsrunning.release()

         # Make copy of shared arrays         
         lockDo.acquire()
         localDo = sharedDo
         sharedDo = None
         lockDo.release()
         
         lockTimeout.acquire()
         timeout = sharedTimeout - time.time()
         lockTimeout.release()
         
         movement = {'names':[], 'times':[], 'keys':[]}
         if localDo != None:
            if self.config.isDebug:
               print("Doing move: ", localDo)

            mvdata = mvdb.get(localDo)
            if mvdata:
               movement = mvdata
            elif sharedTimeout - time.time() <= 0:
               self.config.posture.goToPosture(localDo, 0.2)
               sharedTimeout = 0.2

         if movement['names'] != [] and timeout <= 0:
            lockDone.acquire()
            sharedDone = localDo
            lockDone.release()
            

            if "HeadYaw" in movement["names"] or "HeadPitch" in movement["names"]:
               lockLookat.acquire()
               sharedLookat = None
               lockLookat.release()

            if "HeadYaw" in movement["names"]:
               self.config.motion.setAngles("HeadYaw", movement["keys"][movement["names"].index("HeadYaw")][0][0], 0.2)

            if "HeadPitch" in movement["names"]:
               self.config.motion.setAngles("HeadPitch", movement["keys"][movement["names"].index("HeadPitch")][0][0], 0.2)

            sharedTimeout = time.time() + movement['times'][0][-1] + movement['timeout']
            self.config.motion.angleInterpolationBezier(movement['names'], movement['times'], movement['keys']) # blocking
            sharedTimeout = time.time() + movement['timeout']
         
         time.sleep(0.03)
         lockIsrunning.acquire()
      
      lockIsrunning.release()
      # sit and relax
      self.config.motion.rest()
      print("Quitting movement GENERAL.")



class start:
   def __init__(self, configuration):
      """Starts separate thread for movement control."""
      self.config = configuration
      if configuration.isRecording:
         self.exportFile = open(configuration.exportName + "_motion.txt", 'w') 
      if configuration.motion != None:
         global sharedIsrunning, sharedLLeg
         sharedIsrunning = True
         self.config.posture.goToPosture("Stand", 0.8)
         
         time.sleep(1) # Calibrate view-angle
         sharedLLeg = self.config.memory.getData("Device/SubDeviceList/LHipPitch/Position/Sensor/Value")
         
         headtrackingThread(configuration).start()
         movementThread(configuration).start()
   
   def lastMove(self):
      """Return last action-movement done."""
      global lockDone, sharedDone
      lockDone.acquire()
      localDone = sharedDone
      lockDone.release()
      return localDone
   
   def do(self, move):
      """Change current action-movement. Changes will not take effect until previous move is done."""
      global lockDo, sharedDo
      lockDo.acquire()
      if sharedDo == None:
         sharedDo = move
         if self.config.isRecording:
            self.exportFile.write(time.strftime("%d.%m.%Y %H:%M:%S") + " do("+move+")\n")
         print("Adding move to queue: ", move)
      lockDo.release()   
      
   def doBlocking(self, move, lastMove = False):
      """Same as do, but blocking. :lastmove: determines whether to affect its value (default: False)."""
      global lockDo, sharedDo, sharedTimeout
      global lockDone, sharedDone
      global lockIsrunning
      if self.config.motion != None:
         lockIsrunning.acquire()
         lockDo.acquire()
         lockLookat.acquire()

         if lastMove:
            sharedLookat = None
            sharedDo = None
            lockDone.acquire()
            sharedDone = move
            lockDone.release()

         try:
            if self.config.isRecording:
               self.exportFile.write(time.strftime("%d.%m.%Y %H:%M:%S") + " doBlocking("+move+", "+str(lastMove)+")\n")
               
            timeout = sharedTimeout - time.time()
            if timeout > 0:
               time.sleep(timeout)
 
            sharedTimeout = time.time() + 100
            movement = {'names':[], 'times':[], 'keys':[]}
            if self.config.isDebug:
               print("Doing blocking move: ", move)

            mvdata = mvdb.get(move)
            if mvdata:
               movement = mvdata
               movement["names"] = list(movement["names"])
               movement["keys"] = list(movement["keys"])
               movement["times"] = list(movement["times"])
            else:
               self.config.posture.goToPosture(move, 0.2)
               time.sleep(0.2)

            if movement['names'] != []:
               setJoints = []
               setAngles = []
               if "HeadYaw" in movement["names"]:
                  index = movement["names"].index("HeadYaw")
                  setJoints.append("HeadYaw")
                  setAngles.append(movement["keys"][index][0][0])
                  del movement["names"][index]
                  del movement["keys"][index]
                  del movement["times"][index]
                  
               if "HeadPitch" in movement["names"]:
                  index = movement["names"].index("HeadPitch")
                  setJoints.append("HeadPitch")
                  setAngles.append(movement["keys"][index][0][0])
                  del movement["names"][index]
                  del movement["keys"][index]
                  del movement["times"][index]

               if setJoints != []:
                  self.config.motion.setAngles(setJoints, setAngles, 0.2)
                  
               self.config.motion.angleInterpolationBezier(movement['names'], movement['times'], movement['keys']) # blocking
               time.sleep(movement['timeout'])
         finally:
            sharedTimeout = time.time()
            lockDo.release()
            lockLookat.release()
            lockIsrunning.release()
      
   def lookat(self, position):
      """Changes current look-at position. Position is with TORSO reference frame."""
      global lockLookat, sharedLookat
      lockLookat.acquire()
      if self.config.isRecording and not np.all(sharedLookat == position):
         self.exportFile.write(time.strftime("%d.%m.%Y %H:%M:%S") + " lookat("+str(position)+")\n")
      sharedLookat = position
      lockLookat.release()
   
   def getAngles(self, joints):
      """Return angle values of given joint/chains/.. in radians."""
      if self.config.motion != None:
         return self.config.motion.getAngles(joints, True)
      else:
         return []
   
   def getBodyNames(self, chain):
      """Return joint names for given chain."""
      if self.config.motion != None:
         return self.config.motion.getBodyNames(chain)
      else:
         return []
   
   def getPosition(self, joint, legCorrection = False):
      """Return 6D joint position in TORSO reference frame."""
      global sharedLLeg
      if self.config.motion != None:
         position = self.config.motion.getPosition(joint, 0, True)
         if legCorrection:
            angle = self.config.memory.getData("Device/SubDeviceList/LHipPitch/Position/Sensor/Value") - sharedLLeg
            c, s = np.cos(angle), np.sin(angle)
            newPosition = np.dot(np.array(((c, -s), (s, c))), np.array([[position[0]], [position[2]]]))
            position[0] = newPosition[0,0]
            position[2] = newPosition[1,0]
         return position
      else:
         return [0, 0, 0, 0, 0, 0]
   
   def getTransform(self, joint):
      """Return 4x4 numpy homogenous transformation matrix."""
      if self.config.motion != None:
         T = np.array(self.config.motion.getTransform(joint, 0, True))
         T.shape = (4,4)
      else:
         T = np.eye(4)
      return T
   
   def stop(self):
      """Stop movement thread."""
      global lockIsrunning, sharedIsrunning
      if self.config.isRecording:
         self.exportFile.close()
      if lockIsrunning.acquire(False):
         sharedIsrunning = False
         lockIsrunning.release()
         print("Exit movement.")
      else:
         print("Could not exit movement, locked.")
