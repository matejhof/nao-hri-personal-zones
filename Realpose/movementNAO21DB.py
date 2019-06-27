#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: (moves) Hagen Lehmann, (code) Adam Rojik

moves = {}

names = list()
times = list()
keys = list()

names.append("LElbowRoll")
times.append([0.72, 1.48, 2.16, 2.72, 3.4, 4.52])
keys.append([[-1.37902, [3, -0.24, 0], [3, 0.253333, 0]], [-1.29005, [3, -0.253333, -0.0345436], [3, 0.226667, 0.0309074]], [-1.18267, [3, -0.226667, 0], [3, 0.186667, 0]], [-1.24863, [3, -0.186667, 0.0205524], [3, 0.226667, -0.0249565]], [-1.3192, [3, -0.226667, 0], [3, 0.373333, 0]], [-1.18421, [3, -0.373333, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([0.72, 1.48, 2.16, 2.72, 3.4, 4.52])
keys.append([[-0.803859, [3, -0.24, 0], [3, 0.253333, 0]], [-0.691876, [3, -0.253333, -0.0137171], [3, 0.226667, 0.0122732]], [-0.679603, [3, -0.226667, -0.0122732], [3, 0.186667, 0.0101073]], [-0.610574, [3, -0.186667, 0], [3, 0.226667, 0]], [-0.753235, [3, -0.226667, 0], [3, 0.373333, 0]], [-0.6704, [3, -0.373333, 0], [3, 0, 0]]])

names.append("LHand")
times.append([1.48, 4.52])
keys.append([[0.238207, [3, -0.493333, 0], [3, 1.01333, 0]], [0.240025, [3, -1.01333, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([0.72, 1.48, 2.16, 2.72, 3.4, 4.52])
keys.append([[1.11824, [3, -0.24, 0], [3, 0.253333, 0]], [0.928028, [3, -0.253333, 0], [3, 0.226667, 0]], [0.9403, [3, -0.226667, 0], [3, 0.186667, 0]], [0.862065, [3, -0.186667, 0], [3, 0.226667, 0]], [0.897349, [3, -0.226667, 0], [3, 0.373333, 0]], [0.842125, [3, -0.373333, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([0.72, 1.48, 2.16, 2.72, 3.4, 4.52])
keys.append([[0.363515, [3, -0.24, 0], [3, 0.253333, 0]], [0.226991, [3, -0.253333, 0.0257175], [3, 0.226667, -0.0230104]], [0.20398, [3, -0.226667, 0], [3, 0.186667, 0]], [0.217786, [3, -0.186667, -0.00669692], [3, 0.226667, 0.00813198]], [0.248467, [3, -0.226667, 0], [3, 0.373333, 0]], [0.226991, [3, -0.373333, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([1.48, 4.52])
keys.append([[0.147222, [3, -0.493333, 0], [3, 1.01333, 0]], [0.11961, [3, -1.01333, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([0.64, 1.4, 1.68, 2.08, 2.4, 2.64, 3.04, 3.32, 3.72, 4.44])
keys.append([[1.38524, [3, -0.213333, 0], [3, 0.253333, 0]], [0.242414, [3, -0.253333, 0], [3, 0.0933333, 0]], [0.349066, [3, -0.0933333, -0.0949577], [3, 0.133333, 0.135654]], [0.934249, [3, -0.133333, 0], [3, 0.106667, 0]], [0.680678, [3, -0.106667, 0.141383], [3, 0.08, -0.106037]], [0.191986, [3, -0.08, 0], [3, 0.133333, 0]], [0.261799, [3, -0.133333, -0.0698132], [3, 0.0933333, 0.0488692]], [0.707216, [3, -0.0933333, -0.103967], [3, 0.133333, 0.148524]], [1.01927, [3, -0.133333, -0.0664734], [3, 0.24, 0.119652]], [1.26559, [3, -0.24, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([0.64, 1.4, 2.08, 2.64, 3.32, 3.72, 4.44])
keys.append([[-0.312978, [3, -0.213333, 0], [3, 0.253333, 0]], [0.564471, [3, -0.253333, 0], [3, 0.226667, 0]], [0.391128, [3, -0.226667, 0.0395378], [3, 0.186667, -0.0325606]], [0.348176, [3, -0.186667, 0], [3, 0.226667, 0]], [0.381923, [3, -0.226667, -0.0337477], [3, 0.133333, 0.0198516]], [0.977384, [3, -0.133333, 0], [3, 0.24, 0]], [0.826783, [3, -0.24, 0], [3, 0, 0]]])

names.append("RHand")
times.append([1.4, 3.32, 4.44])
keys.append([[0.853478, [3, -0.466667, 0], [3, 0.64, 0]], [0.854933, [3, -0.64, 0], [3, 0.373333, 0]], [0.425116, [3, -0.373333, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([0.64, 1.4, 2.08, 2.64, 3.32, 4.44])
keys.append([[0.247016, [3, -0.213333, 0], [3, 0.253333, 0]], [-1.17193, [3, -0.253333, 0], [3, 0.226667, 0]], [-1.0891, [3, -0.226667, 0], [3, 0.186667, 0]], [-1.26091, [3, -0.186667, 0], [3, 0.226667, 0]], [-1.14892, [3, -0.226667, -0.111982], [3, 0.373333, 0.184441]], [1.02015, [3, -0.373333, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([0.64, 1.4, 2.08, 2.64, 3.32, 4.44])
keys.append([[-0.242414, [3, -0.213333, 0], [3, 0.253333, 0]], [-0.954191, [3, -0.253333, 0], [3, 0.226667, 0]], [-0.460242, [3, -0.226667, 0], [3, 0.186667, 0]], [-0.960325, [3, -0.186667, 0], [3, 0.226667, 0]], [-0.328317, [3, -0.226667, -0.0474984], [3, 0.373333, 0.0782326]], [-0.250085, [3, -0.373333, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([1.4, 3.32, 4.44])
keys.append([[-0.312978, [3, -0.466667, 0], [3, 0.64, 0]], [-0.303775, [3, -0.64, -0.00920312], [3, 0.373333, 0.00536849]], [0.182504, [3, -0.373333, 0], [3, 0, 0]]])

moves['wave'] = {}
moves['wave']['names'] = names
moves['wave']['times'] = times
moves['wave']['keys'] = keys
moves['wave']['timeout'] = 0



names = list()
times = list()
keys = list()

"""
names.append("HeadPitch")
times.append([0.52, 1.04])
keys.append([[-0.161112, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.161112, [3, -0.173333, 0], [3, 0, 0]]])

names.append("HeadYaw")
times.append([0.52, 1.04])
keys.append([[-0.00464392, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.00464392, [3, -0.173333, 0], [3, 0, 0]]])
"""

names.append("LAnklePitch")
times.append([0.52, 1.04])
keys.append([[0.0106959, [3, -0.173333, 0], [3, 0.173333, 0]], [0.0106959, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LAnkleRoll")
times.append([0.52, 1.04])
keys.append([[-0.105804, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.105804, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LElbowRoll")
times.append([0.52, 1.04])
keys.append([[-0.546061, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.546061, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([0.52, 1.04])
keys.append([[-1.17969, [3, -0.173333, 0], [3, 0.173333, 0]], [-1.17969, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LHand")
times.append([0.52, 1.04])
keys.append([[0.2912, [3, -0.173333, 0], [3, 0.173333, 0]], [0.2912, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LHipPitch")
times.append([0.52, 1.04])
keys.append([[0.444902, [3, -0.173333, 0], [3, 0.173333, 0]], [0.455641, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LHipRoll")
times.append([0.52, 1.04])
keys.append([[0.1335, [3, -0.173333, 0], [3, 0.173333, 0]], [0.1335, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LHipYawPitch")
times.append([0.52, 1.04])
keys.append([[-0.136484, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.131882, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LKneePitch")
times.append([0.52, 1.04])
keys.append([[-0.0890141, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.0890141, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([0.52, 1.04])
keys.append([[1.16733, [3, -0.173333, 0], [3, 0.173333, 0]], [1.16733, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([0.52, 1.04])
keys.append([[-0.116626, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.11049, [3, -0.173333, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([0.52, 1.04])
keys.append([[0.342041, [3, -0.173333, 0], [3, 0.173333, 0]], [0.342041, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RAnklePitch")
times.append([0.52, 1.04])
keys.append([[-0.00302602, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.00302602, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RAnkleRoll")
times.append([0.52, 1.04])
keys.append([[0.12583, [3, -0.173333, 0], [3, 0.173333, 0]], [0.12583, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([0.52, 1.04])
keys.append([[0.770109, [3, -0.173333, 0], [3, 0.173333, 0]], [0.770109, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([0.52, 1.04])
keys.append([[1.10904, [3, -0.173333, 0], [3, 0.173333, 0]], [1.10904, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RHand")
times.append([0.52, 1.04])
keys.append([[0.2944, [3, -0.173333, 0], [3, 0.173333, 0]], [0.2944, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RHipPitch")
times.append([0.52, 1.04])
keys.append([[0.472429, [3, -0.173333, 0], [3, 0.173333, 0]], [0.481634, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RHipRoll")
times.append([0.52, 1.04])
keys.append([[-0.11961, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.11961, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RHipYawPitch")
times.append([0.52, 1.04])
keys.append([[-0.136484, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.131882, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RKneePitch")
times.append([0.52, 1.04])
keys.append([[-0.0889301, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.0889301, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([0.52, 1.04])
keys.append([[1.16588, [3, -0.173333, 0], [3, 0.173333, 0]], [1.16588, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([0.52, 1.04])
keys.append([[0.0981341, [3, -0.173333, 0], [3, 0.173333, 0]], [0.0981341, [3, -0.173333, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([0.52, 1.04])
keys.append([[-0.694945, [3, -0.173333, 0], [3, 0.173333, 0]], [-0.694945, [3, -0.173333, 0], [3, 0, 0]]])

moves['leanback'] = {}
moves['leanback']['names'] = names
moves['leanback']['times'] = times
moves['leanback']['keys'] = keys
moves['leanback']['timeout'] = 1



names = list()
times = list()
keys = list()

names.append("HeadPitch")
times.append([0.8])
keys.append([[-0.0364754, [3, -0.266667, 0], [3, 0, 0]]])

names.append("HeadYaw")
times.append([0.8])
keys.append([[-0.628319, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LAnklePitch")
times.append([0.8])
keys.append([[0.09, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LAnkleRoll")
times.append([0.8])
keys.append([[-0.13, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LElbowRoll")
times.append([0.8])
keys.append([[-1.48231, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([0.8])
keys.append([[-0.720365, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LHand")
times.append([0.8])
keys.append([[0.0304, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LHipPitch")
times.append([0.8])
keys.append([[0.13, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LHipRoll")
times.append([0.8])
keys.append([[0.1, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LHipYawPitch")
times.append([0.8])
keys.append([[-0.17, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LKneePitch")
times.append([0.8])
keys.append([[-0.09, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([0.8])
keys.append([[0.661849, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([0.8])
keys.append([[-0.0330165, [3, -0.266667, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([0.8])
keys.append([[-0.950158, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RAnklePitch")
times.append([0.8])
keys.append([[0.09, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RAnkleRoll")
times.append([0.8])
keys.append([[0.13, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([0.8])
keys.append([[1.44851, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([0.8])
keys.append([[1.06909, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RHand")
times.append([0.8])
keys.append([[0.0248001, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RHipPitch")
times.append([0.8])
keys.append([[0.13, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RHipRoll")
times.append([0.8])
keys.append([[-0.1, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RHipYawPitch")
times.append([0.8])
keys.append([[-0.17, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RKneePitch")
times.append([0.8])
keys.append([[-0.09, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([0.8])
keys.append([[0.171438, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([0.8])
keys.append([[0.207794, [3, -0.266667, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([0.8])
keys.append([[1.00099, [3, -0.266667, 0], [3, 0, 0]]])

moves['startlingleft'] = {}
moves['startlingleft']['names'] = names
moves['startlingleft']['times'] = times
moves['startlingleft']['keys'] = keys
moves['startlingleft']['timeout'] = 0



names = list()
times = list()
keys = list()

names.append("HeadPitch")
times.append([0.76])
keys.append([[0.0215419, [3, -0.253333, 0], [3, 0, 0]]])

names.append("HeadYaw")
times.append([0.76])
keys.append([[0.71384, [3, -0.253333, 0], [3, 0, 0]]])

names.append("LElbowRoll")
times.append([0.76])
keys.append([[-1.52056, [3, -0.253333, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([0.76])
keys.append([[-1.04479, [3, -0.253333, 0], [3, 0, 0]]])

names.append("LHand")
times.append([0.76])
keys.append([[0.0304, [3, -0.253333, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([0.76])
keys.append([[0.251315, [3, -0.253333, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([0.76])
keys.append([[-0.128731, [3, -0.253333, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([0.76])
keys.append([[-1.17432, [3, -0.253333, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([0.76])
keys.append([[1.28139, [3, -0.253333, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([0.76])
keys.append([[0.46999, [3, -0.253333, 0], [3, 0, 0]]])

names.append("RHand")
times.append([0.76])
keys.append([[0.0248001, [3, -0.253333, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([0.76])
keys.append([[0.621937, [3, -0.253333, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([0.76])
keys.append([[0.0476568, [3, -0.253333, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([0.76])
keys.append([[0.792012, [3, -0.253333, 0], [3, 0, 0]]])

moves['startlingright'] = {}
moves['startlingright']['names'] = names
moves['startlingright']['times'] = times
moves['startlingright']['keys'] = keys
moves['startlingright']['timeout'] = 0



names = list()
times = list()
keys = list()

names.append("LAnklePitch")
times.append([1.04])
keys.append([[0.0856071, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LAnkleRoll")
times.append([1.04])
keys.append([[-0.122946, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LElbowRoll")
times.append([1.04])
keys.append([[-0.415279, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([1.04])
keys.append([[-1.19513, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LHand")
times.append([1.04])
keys.append([[0.3, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LHipPitch")
times.append([1.04])
keys.append([[0.13, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LHipRoll")
times.append([1.04])
keys.append([[0.109767, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LHipYawPitch")
times.append([1.04])
keys.append([[-0.17, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LKneePitch")
times.append([1.04])
keys.append([[-0.09, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([1.04])
keys.append([[1.46839, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([1.04])
keys.append([[0.17942, [3, -0.346667, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([1.04])
keys.append([[0.102832, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RAnklePitch")
times.append([1.04])
keys.append([[0.0848469, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RAnkleRoll")
times.append([1.04])
keys.append([[0.13, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([1.04])
keys.append([[0.413034, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([1.04])
keys.append([[1.19272, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RHand")
times.append([1.04])
keys.append([[0.3, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RHipPitch")
times.append([1.04])
keys.append([[0.13, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RHipRoll")
times.append([1.04])
keys.append([[-0.105717, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RHipYawPitch")
times.append([1.04])
keys.append([[-0.17, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RKneePitch")
times.append([1.04])
keys.append([[-0.09, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([1.04])
keys.append([[1.46834, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([1.04])
keys.append([[-0.17933, [3, -0.346667, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([1.04])
keys.append([[0.0903326, [3, -0.346667, 0], [3, 0, 0]]])

moves['standnohead'] = {}
moves['standnohead']['names'] = names
moves['standnohead']['times'] = times
moves['standnohead']['keys'] = keys
moves['standnohead']['timeout'] = 0


names = list()
times = list()
keys = list()

names.append("LElbowRoll")
times.append([0.04, 0.6, 1.24])
keys.append([[-0.905826, [3, -0.0133333, 0], [3, 0.186667, 0]], [-1.54462, [3, -0.186667, 0], [3, 0.213333, 0]], [-1.25784, [3, -0.213333, 0], [3, 0, 0]]])

names.append("LElbowYaw")
times.append([0.04, 0.6, 1.24])
keys.append([[-0.970403, [3, -0.0133333, 0], [3, 0.186667, 0]], [-0.610865, [3, -0.186667, 0], [3, 0.213333, 0]], [-0.790634, [3, -0.213333, 0], [3, 0, 0]]])

names.append("LHand")
times.append([0.04, 0.6, 1.24])
keys.append([[0.3, [3, -0.0133333, 0], [3, 0.186667, 0]], [0.31, [3, -0.186667, 0], [3, 0.213333, 0]], [0.292, [3, -0.213333, 0], [3, 0, 0]]])

names.append("LShoulderPitch")
times.append([0.04, 0.6, 1.24])
keys.append([[1.5865, [3, -0.0133333, 0], [3, 0.186667, 0]], [0.537561, [3, -0.186667, 0.424348], [3, 0.213333, -0.484969]], [-1.14145, [3, -0.213333, 0], [3, 0, 0]]])

names.append("LShoulderRoll")
times.append([0.04, 0.6, 1.24])
keys.append([[0.260054, [3, -0.0133333, 0], [3, 0.186667, 0]], [1.0472, [3, -0.186667, 0], [3, 0.213333, 0]], [0.443284, [3, -0.213333, 0], [3, 0, 0]]])

names.append("LWristYaw")
times.append([0.04, 0.6, 1.24])
keys.append([[-0.0785398, [3, -0.0133333, 0], [3, 0.186667, 0]], [-0.205949, [3, -0.186667, 0.0636711], [3, 0.213333, -0.072767]], [-0.487854, [3, -0.213333, 0], [3, 0, 0]]])

names.append("RElbowRoll")
times.append([0.04, 1.24])
keys.append([[0.0445281, [3, -0.0133333, 0], [3, 0.4, 0]], [0.136568, [3, -0.4, 0], [3, 0, 0]]])

names.append("RElbowYaw")
times.append([0.04, 1.24])
keys.append([[1.30999, [3, -0.0133333, 0], [3, 0.4, 0]], [0.67952, [3, -0.4, 0], [3, 0, 0]]])

names.append("RHand")
times.append([0.04, 1.24])
keys.append([[0.2848, [3, -0.0133333, 0], [3, 0.4, 0]], [0.2892, [3, -0.4, 0], [3, 0, 0]]])

names.append("RShoulderPitch")
times.append([0.04, 1.24])
keys.append([[1.24872, [3, -0.0133333, 0], [3, 0.4, 0]], [1.30394, [3, -0.4, 0], [3, 0, 0]]])

names.append("RShoulderRoll")
times.append([0.04, 1.24])
keys.append([[0.00455999, [3, -0.0133333, 0], [3, 0.4, 0]], [0.052114, [3, -0.4, 0], [3, 0, 0]]])

names.append("RWristYaw")
times.append([0.04, 1.24])
keys.append([[-1.24258, [3, -0.0133333, 0], [3, 0.4, 0]], [0.0352399, [3, -0.4, 0], [3, 0, 0]]])

moves['calibration'] = {}
moves['calibration']['names'] = names
moves['calibration']['times'] = times
moves['calibration']['keys'] = keys
moves['calibration']['timeout'] = 0.2

# Exported keys from choregraphe -> keyframesToMotion -> here
moves.update({'calibration0': {'keys': [[[-1.26858, [3, -0.0133333, 0], [3, 0.08, 0]]], [[-0.794654, [3, -0.0133333, 0], [3, 0.08, 0]]], [[0.3024, [3, -0.0133333, 0], [3, 0.08, 0]]], [[-1.09532, [3, -0.0133333, 0], [3, 0.08, 0]]], [[0.47243, [3, -0.0133333, 0], [3, 0.08, 0]]], [[-0.47098, [3, -0.0133333, 0], [3, 0.08, 0]]], [[0.130432, [3, -0.0133333, 0], [3, 0.08, 0]]], [[0.700996, [3, -0.0133333, 0], [3, 0.08, 0]]], [[0.2892, [3, -0.0133333, 0], [3, 0.08, 0]]], [[1.22724, [3, -0.0133333, 0], [3, 0.08, 0]]], [[0.00455999, [3, -0.0133333, 0], [3, 0.08, 0]]], [[0.026036, [3, -0.0133333, 0], [3, 0.08, 0]]]], 'names': ['LElbowRoll', 'LElbowYaw', 'LHand', 'LShoulderPitch', 'LShoulderRoll', 'LWristYaw', 'RElbowRoll', 'RElbowYaw', 'RHand', 'RShoulderPitch', 'RShoulderRoll', 'RWristYaw'], 'timeout': 0.2, 'times': [[1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04]]}, 'calibration1': {'keys': [[[-1.54462, [3, -0.08, 0], [3, 0.106667, 0]]], [[0.08126, [3, -0.08, 0], [3, 0.106667, 0]]], [[0.3024, [3, -0.08, 0], [3, 0.106667, 0]]], [[-1.09532, [3, -0.08, 0], [3, 0.106667, 0]]], [[1.2517, [3, -0.08, 0], [3, 0.106667, 0]]], [[-0.841249, [3, -0.08, 0], [3, 0.106667, 0]]], [[0.130432, [3, -0.08, 0], [3, 0.106667, 0]]], [[0.700996, [3, -0.08, 0], [3, 0.106667, 0]]], [[0.2892, [3, -0.08, 0], [3, 0.106667, 0]]], [[1.22724, [3, -0.08, 0], [3, 0.106667, 0]]], [[0.00455999, [3, -0.08, 0], [3, 0.106667, 0]]], [[0.026036, [3, -0.08, 0], [3, 0.106667, 0]]]], 'names': ['LElbowRoll', 'LElbowYaw', 'LHand', 'LShoulderPitch', 'LShoulderRoll', 'LWristYaw', 'RElbowRoll', 'RElbowYaw', 'RHand', 'RShoulderPitch', 'RShoulderRoll', 'RWristYaw'], 'timeout': 0.2, 'times': [[1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04]]}, 'calibration2': {'keys': [[[-0.315962, [3, -0.106667, 0], [3, 0.133333, 0]]], [[-0.090548, [3, -0.106667, 0.171808], [3, 0.133333, -0.21476]]], [[0.3024, [3, -0.106667, 0], [3, 0.133333, 0]]], [[-0.193326, [3, -0.106667, -0.316799], [3, 0.133333, 0.395999]]], [[0.162562, [3, -0.106667, 0], [3, 0.133333, 0]]], [[-0.673468, [3, -0.106667, -0.125078], [3, 0.133333, 0.156347]]], [[0.130432, [3, -0.106667, 0], [3, 0.133333, 0]]], [[0.690258, [3, -0.106667, 0], [3, 0.133333, 0]]], [[0.2892, [3, -0.106667, 0], [3, 0.133333, 0]]], [[1.22724, [3, -0.106667, 0], [3, 0.133333, 0]]], [[-0.04913, [3, -0.106667, 0.0109084], [3, 0.133333, -0.0136356]]], [[0.026036, [3, -0.106667, 0], [3, 0.133333, 0]]]], 'names': ['LElbowRoll', 'LElbowYaw', 'LHand', 'LShoulderPitch', 'LShoulderRoll', 'LWristYaw', 'RElbowRoll', 'RElbowYaw', 'RHand', 'RShoulderPitch', 'RShoulderRoll', 'RWristYaw'], 'timeout': 0.2, 'times': [[1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04]]}, 'calibration3': {'keys': [[[-0.315962, [3, -0.133333, 0], [3, 0.16, 0]]], [[-1.54018, [3, -0.133333, 0.302152], [3, 0.16, -0.362582]]], [[0.3024, [3, -0.133333, 0], [3, 0.16, 0]]], [[1.04308, [3, -0.133333, -0.0102268], [3, 0.16, 0.0122721]]], [[0.889678, [3, -0.133333, 0], [3, 0.16, 0]]], [[0.00302601, [3, -0.133333, -0.271472], [3, 0.16, 0.325766]]], [[0.130432, [3, -0.133333, 0], [3, 0.16, 0]]], [[0.690258, [3, -0.133333, 0], [3, 0.16, 0]]], [[0.2892, [3, -0.133333, 0], [3, 0.16, 0]]], [[1.22724, [3, -0.133333, 0], [3, 0.16, 0]]], [[-0.069072, [3, -0.133333, 0.00464848], [3, 0.16, -0.00557817]]], [[0.0367742, [3, -0.133333, 0], [3, 0.16, 0]]]], 'names': ['LElbowRoll', 'LElbowYaw', 'LHand', 'LShoulderPitch', 'LShoulderRoll', 'LWristYaw', 'RElbowRoll', 'RElbowYaw', 'RHand', 'RShoulderPitch', 'RShoulderRoll', 'RWristYaw'], 'timeout': 0.2, 'times': [[1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04]]}, 'calibration4': {'keys': [[[-0.677986, [3, -0.16, 0], [3, 0.133333, 0]]], [[-2.08475, [3, -0.16, 0], [3, 0.133333, 0]]], [[0.3024, [3, -0.16, 0], [3, 0.133333, 0]]], [[1.05535, [3, -0.16, -0.0122721], [3, 0.133333, 0.0102268]]], [[-0.104354, [3, -0.16, 0], [3, 0.133333, 0]]], [[1.11824, [3, -0.16, 0], [3, 0.133333, 0]]], [[0.130432, [3, -0.16, 0], [3, 0.133333, 0]]], [[0.690258, [3, -0.16, 0], [3, 0.133333, 0]]], [[0.2892, [3, -0.16, 0], [3, 0.133333, 0]]], [[1.22724, [3, -0.16, 0], [3, 0.133333, 0]]], [[-0.0798099, [3, -0.16, 0], [3, 0.133333, 0]]], [[0.0367742, [3, -0.16, 0], [3, 0.133333, 0]]]], 'names': ['LElbowRoll', 'LElbowYaw', 'LHand', 'LShoulderPitch', 'LShoulderRoll', 'LWristYaw', 'RElbowRoll', 'RElbowYaw', 'RHand', 'RShoulderPitch', 'RShoulderRoll', 'RWristYaw'], 'timeout': 0.2, 'times': [[1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04]]}, 'calibration5': {'keys': [[[-0.208582, [3, -0.133333, -0.0931999], [3, 0.173333, 0.12116]]], [[-2.08475, [3, -0.133333, 0], [3, 0.173333, 0]]], [[0.3024, [3, -0.133333, 0], [3, 0.173333, 0]]], [[1.3913, [3, -0.133333, -0.144507], [3, 0.173333, 0.187859]]], [[0.167164, [3, -0.133333, 0], [3, 0.173333, 0]]], [[0.524586, [3, -0.133333, 0.11405], [3, 0.173333, -0.148264]]], [[0.130432, [3, -0.133333, 0], [3, 0.173333, 0]]], [[0.690258, [3, -0.133333, 0], [3, 0.173333, 0]]], [[0.2892, [3, -0.133333, 0], [3, 0.173333, 0]]], [[1.22724, [3, -0.133333, 0], [3, 0.173333, 0]]], [[-0.0798099, [3, -0.133333, 0], [3, 0.173333, 0]]], [[0.0367742, [3, -0.133333, 0], [3, 0.173333, 0]]]], 'names': ['LElbowRoll', 'LElbowYaw', 'LHand', 'LShoulderPitch', 'LShoulderRoll', 'LWristYaw', 'RElbowRoll', 'RElbowYaw', 'RHand', 'RShoulderPitch', 'RShoulderRoll', 'RWristYaw'], 'timeout': 0.2, 'times': [[1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04]]}, 'calibration6': {'keys': [[[-0.0349066, [3, -0.173333, 0], [3, 0.2, 0]]], [[-2.08475, [3, -0.173333, 0], [3, 0.2, 0]]], [[0.3024, [3, -0.173333, 0], [3, 0.2, 0]]], [[2.05245, [3, -0.173333, 0], [3, 0.2, 0]]], [[0.032172, [3, -0.173333, 0], [3, 0.2, 0]]], [[0.331302, [3, -0.173333, 0.0401214], [3, 0.2, -0.0462939]]], [[0.130432, [3, -0.173333, 0], [3, 0.2, 0]]], [[0.690258, [3, -0.173333, 0], [3, 0.2, 0]]], [[0.2892, [3, -0.173333, 0], [3, 0.2, 0]]], [[1.22724, [3, -0.173333, 0], [3, 0.2, 0]]], [[-0.0798099, [3, -0.173333, 0], [3, 0.2, 0]]], [[0.0367742, [3, -0.173333, 0], [3, 0.2, 0]]]], 'names': ['LElbowRoll', 'LElbowYaw', 'LHand', 'LShoulderPitch', 'LShoulderRoll', 'LWristYaw', 'RElbowRoll', 'RElbowYaw', 'RHand', 'RShoulderPitch', 'RShoulderRoll', 'RWristYaw'], 'timeout': 0.2, 'times': [[1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04]]}, 'calibration7': {'keys': [[[-0.248466, [3, -0.2, 0], [3, 0, 0]]], [[-2.08567, [3, -0.2, 0], [3, 0, 0]]], [[0.3024, [3, -0.2, 0], [3, 0, 0]]], [[1.72571, [3, -0.2, 0], [3, 0, 0]]], [[0.400332, [3, -0.2, 0], [3, 0, 0]]], [[0.26534, [3, -0.2, 0], [3, 0, 0]]], [[0.130432, [3, -0.2, 0], [3, 0, 0]]], [[0.690258, [3, -0.2, 0], [3, 0, 0]]], [[0.2892, [3, -0.2, 0], [3, 0, 0]]], [[1.22724, [3, -0.2, 0], [3, 0, 0]]], [[-0.0798099, [3, -0.2, 0], [3, 0, 0]]], [[0.0367742, [3, -0.2, 0], [3, 0, 0]]]], 'names': ['LElbowRoll', 'LElbowYaw', 'LHand', 'LShoulderPitch', 'LShoulderRoll', 'LWristYaw', 'RElbowRoll', 'RElbowYaw', 'RHand', 'RShoulderPitch', 'RShoulderRoll', 'RWristYaw'], 'timeout': 0.2, 'times': [[1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04], [1.04]]}})


del names,times,keys

def get(move):
   """Movements database. Returns exported movements from Choregraphe in format for angleInterpolationBezier from NAOqi + timeout delay after move.
   If movement is not in DB, returns False."""
   if move in moves:
      return dict(moves[move])
   return False
   
def list():
   """Returns list of avalaible movements."""
   return moves.keys()