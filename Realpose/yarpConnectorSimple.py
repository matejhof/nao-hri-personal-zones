#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Lukáš Rustler, Adam Rojík
import yarp
import threading
import time

# add logging

sharedIsrunning = False
sharedIsrunningLock = threading.Condition()

sharedTouchside = None
sharedTouchsideLock = threading.Condition()

sharedTouchsideraw = None
sharedTouchsiderawLock = threading.Condition()

class skinConfig():
   def __init__(self):
      self.status = True
      self.exportName = ""
      self.isDebug = False
      self.isRecording = False
      self.startTime = time.time()

class skinThread(threading.Thread):
   def __init__(self, configuration):
      threading.Thread.__init__(self)
      self.name = "skinThread"
      self.config = configuration
      self.skinPart = "SKIN_PART_UNKNOWN, left_hand, SKIN_LEFT_FOREARM, SKIN_LEFT_UPPER_ARM, right_hand, head, SKIN_RIGHT_UPPER_ARM, torso, LEFT_LEG_UPPER, LEFT_LEG_LOWER, LEFT_FOOT, RIGHT_LEG_UPPER, RIGHT_LEG_LOWER, RIGHT_FOOT, SKIN_PART_ALL, SKIN_PART_SIZE".split(", ")
      if self.config.status:
         try:
            if self.config.isRecording:
               self.lastTouchside = False
               self.exportTouch = open(self.config.exportName + "_touch.py", 'w')
               self.exportTouch.write("times = []\n")
               self.exportTouch.write("side = []\n")

            yarp.Network.init() # Init yarp
            self.manager = yarp.BufferedPortBottle()  # init Bottle
            self.manager.open("/skinManager")  # Open new port
            yarp.Network.connect("/skinManager/skin_events:o", "/skinManager")  # connect Nao port with virtual port
         except:
            sharedIsrunningLock.acquire()
            sharedIsrunning = False
            sharedIsrunningLock.release()

   def run(self):
      global sharedIsrunningLock, sharedIsrunning
      global sharedTouchsideLock, sharedTouchside
      global sharedTouchsideraw, sharedTouchsiderawLock

      try:
         sharedIsrunningLock.acquire()
         while sharedIsrunning:
            sharedIsrunningLock.release()
         
            localTouchside = self.whichSide(self.readRaw(3))
         
            if localTouchside != None:
               sharedTouchsideLock.acquire()
               sharedTouchside = localTouchside
               sharedTouchsideLock.release()


            if self.config.isRecording and localTouchside != self.lastTouchside:
               sharedTouchsiderawLock.acquire()
               sharedTouchsideraw = localTouchside
               sharedTouchsiderawLock.release()
               
               timer = time.time() - self.config.startTime
               self.exportTouch.write("times.append(" + str(timer)+ ")\n")
               self.exportTouch.write("side.append(" + str(localTouchside)+ ")\n")
               self.lastTouchside = localTouchside
            
            time.sleep(0.1)
            sharedIsrunningLock.acquire()
      finally:
         if self.config.isRecording:
            self.exportTouch.close()
         self.manager.close()
         try:
            sharedIsrunningLock.release()
         except:
            pass
         print("Quitting skin.")


   def readRaw(self, thresholdTaxels=0):
      """Read raw data from skin in parsed array. Filters out touches with less than :thresholdTaxels: pressed."""
      if not self.config.status:
         return []

      data = self.manager.read()
      data = data.toString()

      output = []
      if data != "":
         splitData = data[1:-1].replace(") (", ";")[1:].split(") ")
         splitData[0] = splitData[0].split(";")
         for i in range(len(splitData[0])):
            splitData[0][i] = splitData[0][i].split(" ")
      
         #if splitData[0][0][3] == '1': # Broken sensors filter
         #   splitData[0][-1] = filter(lambda x: x not in ['1', '2', '4', '5', '6', '7', '8', '9'], splitData[0][-1])
      
         if len(splitData[0][-1]) > thresholdTaxels:
            output = splitData
      return output


   def whichSide(self, data):
      """Return which side from raw data. (-1 left, 0 center, 1 right)"""
      if not self.config.status:
         return None

      if data == []:
         return None
      bodyPart = int(data[0][0][3])
      if bodyPart == self.skinPart.index("left_hand"):
         return -1
      elif bodyPart == self.skinPart.index("right_hand"):
         return 1
      return 0



class start:
   """Class for reading data from skin."""
   def __init__(self, configuration):
      global sharedIsrunning
      self.config = configuration
      if self.config.status:
         sharedIsrunning = True
         skinThread(self.config).start()

   def whichSide(self, raw = False):
      global sharedTouchside, sharedTouchsideLock
      global sharedTouchsideraw, sharedTouchsiderawLock
      if raw:
         sharedTouchsiderawLock.acquire()
         localTouchside = sharedTouchsideraw
         sharedTouchsiderawLock.release()
      else:
         sharedTouchsideLock.acquire()
         localTouchside = sharedTouchside
         sharedTouchside = None
         sharedTouchsideLock.release()
      return localTouchside
            
   def stop(self):
      global sharedIsrunning, sharedIsrunningLock
      if sharedIsrunningLock.acquire(False):
         sharedIsrunning = False
         sharedIsrunningLock.release()
         print("Exit skin.")
      else:
         print("Could not exit skin, locked")
