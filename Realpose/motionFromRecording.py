from __future__ import print_function
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Adam Rojik
import datetime

firstDate = None
lastDate = None
words = {}
scenes = ["recordings/19-06-12_18-17-21_SCENE-1_motion.txt", "recordings/19-06-12_18-20-09_SCENE-2_motion.txt"]
totalTime = datetime.timedelta(0)
lastAction = None
lastLookat = None
for scene in scenes:
   with open(scene) as file:
      for row in file:
         data = row.split(" ")
         lastDate = datetime.datetime.strptime(data[0]+' '+data[1], '%d.%m.%Y %H:%M:%S')
         if firstDate == None:
            firstDate = lastDate
         actionList = data[2].split("(")
         action = actionList[0]
         if action == 'do':
            value = actionList[1][:-2]
            if value != lastAction:
               lastAction = value
               print(value, lastDate - firstDate)
               if value in words:
                  words[value] += 1
               else:
                  words[value] = 1
         else:
            lookat = row.split("(")[1][:-2]
            if lookat != lastLookat:
               #print(lastLookat, lookat)
               lastLookat = lookat
               if action in words:
                  words[action] += 1
               else:
                  words[action] = 1
   totalTime += lastDate - firstDate
for word in words:
   print(word + " every " + str(totalTime.seconds/words[word]) + "s")
print(totalTime.seconds, words)