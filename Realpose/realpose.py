from __future__ import print_function
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Adam Rojik

##### Imports
import sys, getopt
import os
import numpy as np
import datetime as dt
import time
import math
import json
from collections import deque

import videoPose as vid
import movementNAO21 as movement
import yarpConnectorSimple as skinRead


### Robot
# camera calibration
toRobRotation = np.eye(3)
toRobTranslation = np.array([0, 0, 0])
# connection
robotIP = "192.168.210.98"
robotPort = 9559

##### Program
isDebug = False
isView = True
startup = True
isRecording = False
recordDir = "unspecified"

## DEFAULT SCENE
SCENE = 1

try:
   opts, args = getopt.getopt(sys.argv[1:], "hdo:c:s:i:p:",["help", "debug", "output=", "calibration=", "scene=", "ip=", "port="])
except getopt.GetoptError as e:
   print(e)
   sys.exit(2)

for opt,arg in opts:
   if opt == '-d' or opt == '--debug':
      isDebug = True
      print("Debug mode activated.")
   elif opt == '-i' or opt == '--ip':
      robotIP = arg
   elif opt == '-p' or opt == '--port':
      robotPort = int(arg)
   elif opt == '-s' or opt == '--scene':
      tryScene = int(arg)
      if not tryScene in range(1,5):
         print("Wrong scene, keeping default")
      else:
         SCENE = tryScene
   elif opt == '-o' or opt == '--output':
      recordDir = arg
      isRecording = True
      print('Recording output to folder: "'+recordDir+'".')
   elif opt == '-c' or opt == '--calibration':
      try:
         calibration = json.loads(arg)
         toRobRotation = np.array(calibration[0])
         toRobTranslation = np.array(calibration[1])
         toRobRotation.shape = (3,3)
         
         startup = False
         print("Imported calibration.")
      except:
         print("Unable to process calibration string, ignoring argument.")
   elif opt == '-h' or opt == '--help':
      print("Help:")
      print("--help -h (this)")
      print('--debug -d (activate debug mode)')
      print('--scene -s (load scene 1 = CONTROL, 2 = LEAN BACK + NAO LIMITS, 3 = LEAN BACK + HUMAN LIMITS, 4 = TOUCH + HUMAN LIMITS, 5 = TOUCH + NO REACTION)')
      print('--output -o "'+recordDir+'" (dir for recorded output, recording - touches, nao angles, realsense, video output)')
      print('--calibration -c "'+json.dumps([toRobRotation.tolist(), toRobTranslation.tolist()])+'" (load exported calibration)')
      print('--ip -i "'+robotIP+'" (NAOs IP address, get from "ping smurf.local")')
      print('--port -p "'+str(robotPort)+'" (NAOs port, should not change, but from Choregraphe)')
      sys.exit(0)

#### Scene set
# 1 = CONTROL
# 2 = LEANBACK + NAO LIMITS
# 3 = LEANBACK + HUMAN LIMITS
# 4 = TOUCH + HUMAN LIMITS
# 5 = TOUCH + NO REACTION
print("Running SCENE", SCENE)
selectedZone = 'HUMAN'
if SCENE in [2]:
   selectedZone = 'NAO'

allowLeanback = False
allowTouch = True
allowHeadTracking = False
allowHeadTrackingStopOnLeave = True
allowHeadTrackingStartOnTouch = True
if SCENE in [1, 2, 3]:
   allowLeanback = True
   allowTouch = False
   allowHeadTracking = True
   allowHeadTrackingStopOnLeave = False
   allowHeadTrackingStartOnTouch = False

if SCENE in [5]:
   allowTouch = False

allowWave = False # Disabled for being too expressive
print("ZONE:", selectedZone, "Leanback", allowLeanback, "Touch:", allowTouch, "Wave:", allowWave)

windowTreshold = .5

# Zones
ZONES = { # in meters (intimate, personal, social)
      'NAO': [0.16, 0.42, 1.27],
      'HUMAN': [0.45, 1.2, 3.7]
}
ZONE = ZONES[selectedZone]

# ROBOT
ROBOT = {
   'vision': {},
   'touch': {
      'side': None
   }
}

if isRecording:
   outputFolder = "recordings/" + recordDir
   if not os.path.exists(outputFolder):
      os.mkdir(outputFolder)
   print('Recording into "'+recordDir+'" folder')
   exportName = outputFolder + "/" + time.strftime("%y-%m-%d_%H-%M-%S")+"_SCENE-"+str(SCENE)
else:
   exportName = ""
startTime = time.time()


# Movements
mvConfig = movement.config()
if not mvConfig.connect(robotIP, robotPort):
   print("Robot not connected.")
else:
   mvConfig.setupSafeMotion(robotIP, robotPort)
mvConfig.debug = isDebug
mvConfig.isRecording = isRecording
mvConfig.exportName = exportName
mvConfig.startTime = startTime
mv = movement.start(mvConfig)


skinConfig = skinRead.skinConfig()
skinConfig.isDebug = isDebug
skinConfig.isRecording = isRecording
skinConfig.exportName = exportName
skinConfig.startTime = startTime
skinConfig.status = allowTouch

skin = skinRead.start(skinConfig)


vidConfig = vid.videoConfig()
vidConfig.startup = startup
vidConfig.ZONE = ZONE
vidConfig.SCENE = SCENE
vidConfig.motion = mv
vidConfig.isView = isView
vidConfig.isDebug = isDebug
vidConfig.isRecording = isRecording
vidConfig.exportName = exportName
vidConfig.startTime = startTime
vidConfig.skin = skin
if not startup:
   vidConfig.toRobRotation = toRobRotation
   vidConfig.toRobTranslation = toRobTranslation

video = vid.start(vidConfig)

np.random.seed()
rnNextTime = [time.time()]*2
rnNextTime[1] = time.time() + 20.
prevZone = 4
requestedMove = 'standnohead'

totalWindowTime = 0
lastTimestep = 0
zonesWindow = deque([])
timesWindow = deque([])

try:
   while video.isRunning():
      ROBOT['touch']['side'] = skin.whichSide()
      ROBOT['vision'] = video.getVision()
      
      if ROBOT['touch']['side'] != None:
         ROBOT['vision']['zone']['current'] = 0

      ROBOT['vision']['zone']['velocity'] = prevZone - ROBOT['vision']['zone']['current']
      prevZone = ROBOT['vision']['zone']['current']
      
      # ROBOT reactions
      lastMove = mv.lastMove() # do not use directly, locks variable

      if lastMove in ['startlingleft', 'startlingright', 'startlingcenter'] and allowHeadTrackingStartOnTouch:
         allowHeadTracking = True

      if SCENE == 1: # Control - random movement
         t = time.time()
         if t > rnNextTime[0]:
            rnNextTime[0] = time.time() + np.random.normal(loc=5.0, scale=1.0, size=None)
            x = np.random.random()*20-10
            y = np.random.random()*20-10
            mv.lookat([5, x, y])
         
         if t > rnNextTime[1]:
            if lastMove == 'standnohead':
               rnNextTime[1] = time.time() + 5.
               requestedMove = 'leanback'
            else:
               rnNextTime[1] = time.time() + 20.
               requestedMove = 'standnohead'

         if requestedMove != lastMove:
            mv.do(requestedMove)

      elif SCENE == 5:
         pass
      else:
         t = time.time()
         if lastTimestep != 0:
            tdiff = t - lastTimestep

            while totalWindowTime - tdiff > windowTreshold:
               totalWindowTime -= timesWindow.pop()
               zonesWindow.pop()

            totalWindowTime += tdiff
            timesWindow.appendleft(tdiff)
            zonesWindow.appendleft(ROBOT['vision']['zone']['current'])
         lastTimestep = t

         if ROBOT['vision']['zone']['velocity'] < 0 and ROBOT['vision']['zone']['current'] == 3 and lastMove != 'wave': # getting closer
            if allowWave:
               mv.do('wave')
            
         if ROBOT['vision']['zone']['current'] == 0: # touch
            if allowTouch:
               if allowHeadTrackingStartOnTouch:
                  allowHeadTracking = False
            
               mv.lookat(None)
            
               if ROBOT['touch']['side'] == -1 and lastMove in ['standnohead', 'startlingleft']:
                  mv.doBlocking('startlingleft', True)
               elif ROBOT['touch']['side'] == 0 and lastMove in ['standnohead', 'startlingcenter']:
                  mv.doBlocking('startlingcenter', True)
               elif ROBOT['touch']['side'] == 1 and lastMove in ['standnohead', 'startlingright']:
                  mv.doBlocking('startlingright', True)
               else:
                  mv.doBlocking('standnohead', True)
                  if ROBOT['touch']['side'] == -1:
                     mv.doBlocking('startlingleft', True)
                  elif ROBOT['touch']['side'] == 0:
                     mv.doBlocking('startlingcenter', True)
                  elif ROBOT['touch']['side'] == 1:
                     mv.doBlocking('startlingright', True)
         
         elif ROBOT['vision']['zone']['current'] == 1: # intimate
            if allowLeanback:
               #if totalWindowTime >= windowTreshold and len(filter(lambda x: x == 1, zonesWindow))/len(zonesWindow) > .9:
               mv.do('leanback')
         elif ROBOT['vision']['zone']['current'] > 1 and lastMove != 'standnohead':
            if lastMove in ['startlingleft', 'startlingright', 'startlingcenter']:
               mv.doBlocking('standnohead', True)
            else:
               mv.do('standnohead')
   
         currentMove = mv.lastMove()
         if currentMove in ['standnohead', 'leanback'] and lastMove in ['standnohead', 'leanback']:
            if ROBOT['vision']['zone']['current'] <= 2 and ROBOT['vision']['zone']['current'] > 0:
               if allowHeadTracking and ROBOT['vision']['zone']['current'] != 0 and ROBOT['vision']['objects']['nose']['current']:
                  mv.lookat(ROBOT['vision']['objects']['nose']['coords'])
            elif ROBOT['vision']['zone']['current'] > 2:
               if allowHeadTracking:
                  mv.lookat([10, .01, .01])
               if allowHeadTrackingStopOnLeave:
                  allowHeadTracking = False

finally:
   print("Stopping everything.")
   video.stop()
   mv.stop()
   skin.stop()
