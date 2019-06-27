from naoqi import ALProxy
from collections import OrderedDict
import numpy as np
from heapq import heappush, heappop
import math
import time
#import pickle
class safeMotion:
    def __init__(self, ip="192.168.210.61", port=9559, jointLimits="/home/rustli/NAO/Code/Constraints/data/no-shoulders/limits/checkedSafe.csv", headLimits="/home/rustli/NAO/Code/Constraints/data/no-shoulders/limits/headSafe.csv", currentLimits="/home/rustli/NAO/Code/Constraints/data/no-shoulders/limits/currentMax.csv", safePositions="/home/rustli/NAO/safePositions.pickle"):
        """Creates connection with NAO and loads joint and head limits from CSV.
        
        Joint limits should be separated by new line. Line should contain name;min;max in this format.
        Head limits should be separated by new line. Line should contain postions for HeadYaw;<min HeadPitch>;<max HeadPitch> in this format.
        
        Keyword arguments:
        ip -- NAOs ip (default "192.168.210.60")
        port -- NAOs port proxy (default 9559)
        jointLimits -- path to joint limits csv (default "data/no-shoulders/limits/checked.csv")
        headLimits -- path to joint limits csv (default "data/no-shoulders/limits/headSafe.csv")
        currentLimits -- path to current limits csv (default "data/no-shoulders/limits/currentMax.csv")"""
        
        self.ip = ip
        self.port = port
        self.memory = ALProxy("ALMemory", ip, port)
        self.motion = ALProxy("ALMotion", ip, port)
        self.jointLimits = OrderedDict()
        self.headLimits = OrderedDict()
        self.currentLimits = OrderedDict()
        self.headYawPoints = []
        self.headJoints = ["HeadYaw", "HeadPitch"]
        self.safePositions=None#pickle.load(open(safePositions,"rb"))
        with open(headLimits) as file:
            for line in file:
                try:
                    data = line.split("\n")[0].split(";")
                    index = float(data[0])
                    self.headYawPoints.append(index)
                    self.headLimits[str(index)] = np.array([float(data[1]), float(data[2])])
                except:
                    break

        with open(jointLimits) as file:
            for line in file:
                try:
                    data = line.split("\n")[0].split(";")
                    self.jointLimits[data[0]] = [float(data[1]), float(data[2])]
                except:
                    break

        with open(currentLimits) as file:
            for line in file:
                try:
                    data = line.split("\n")[0].split(";")
                    self.currentLimits[data[0]] = float(data[1])
                except:
                    break
        pass



    def headPitchLimitsAtYaw(self, yaw):
        """Returns array [min, max] positions for HeadPitch at given HeadYaw position.
        If yaw is not within HeadYaw limits, IndexError is raised.
    
        yaw -- HeadYaw angle in radians"""
        if yaw in self.headYawPoints:
            return self.headLimits[str(yaw)]
        
        min = float("-inf")
        max = float("inf")
        for point in self.headYawPoints:
            diff = point - yaw
            if diff < 0:
                if diff > min:
                    min = diff
                    pointA = point
            elif diff < max:
                max = diff
                pointB = point # A < headYawPosition < B

        try:        
            diffX = yaw - pointA
            diffY = self.headLimits[str(pointB)] - self.headLimits[str(pointA)]
        except NameError:
            raise IndexError("HeadPitch limits for given HeadYaw angle are not defined.")
        
        limits = self.headLimits[str(pointA)] + (diffX / (pointB - pointA)) * diffY
        return limits



    def headYawLimits(self, yaw, pitch):
        """Returns array [min, max] positions for HeadYaw at given position.
        Requires both head positions as input, because resulting area is not continuous.
        Raises IndexError if etiher joint is outside defined limits.
    
        yaw -- HeadYaw angle in radians
        pitch -- HeadPitch angle in radians"""
        yaw = float(yaw)
        pitch = float(pitch)
        neighbours = [[], [], []]
        totalYawLimits = [float("inf"), float("-inf")]
        for point in self.headYawPoints:
            if point < totalYawLimits[0]:
                totalYawLimits[0] = point
            elif point > totalYawLimits[1]:
                totalYawLimits[1] = point
            
            diff = point - yaw
            index = 0
            if diff > 0:
                index = 1
            elif diff == 0:
                index = 2
            heappush(neighbours[index], (abs(diff), point))
            
        if yaw < totalYawLimits[0] or yaw > totalYawLimits[1]:
            raise IndexError("HeadPitch limits for given HeadYaw angle are not defined.")
            
        mainPitchLimits = self.headPitchLimitsAtYaw(yaw)
        if pitch < mainPitchLimits[0] or pitch > mainPitchLimits[1]:
            raise IndexError("HeadPitch is outside limits for given HeadYaw.")
        
        limits = [yaw, yaw]
        for side in [0,1]:
            lastPitchLimits = mainPitchLimits
            lastPointYaw = yaw
            while neighbours[side] != []:
                pointYaw = heappop(neighbours[side])[1]
                pitchLimits = self.headLimits[str(pointYaw)]
                if pitch >= pitchLimits[0] and pitch <= pitchLimits[1]:
                    lastPointYaw = pointYaw
                    lastPitchLimits = pitchLimits
                else:
                    index = 0
                    if pitch <= lastPitchLimits[1] and pitch > pitchLimits[1]:
                        index = 1
                    scale = (pitch - lastPitchLimits[index])/(pitchLimits[index] - lastPitchLimits[index])
                    limits[side] = lastPointYaw + (pointYaw - lastPointYaw) * scale
                    break
            if neighbours[side] == []:
                limits[side] = lastPointYaw
        return limits



    def checkJointMove(self, joint, angle, speed=0.):
        """Returns True if given joint angle (rad) lies within its limits. False otherwise.
        Raises IndexError if joint is not loaded.
        
        joint -- name of the joint
        angle -- desired angle in radians
        speed -- fraction of maximum speed to use"""
        
        if joint == "HeadYaw":
            headYawPositoin = self.memory.getData("Device/SubDeviceList/HeadYaw/Position/Sensor/Value")
            headPitchPositoin = self.memory.getData("Device/SubDeviceList/HeadPitch/Position/Sensor/Value")
            try:
                limits = self.headYawLimits(headYawPositoin, headPitchPositoin)
            except IndexError:
                return False
            if angle > limits[0] and angle < limits[1]:
                return True
            
        elif joint == "HeadPitch":
            headYawPosition = self.memory.getData("Device/SubDeviceList/HeadYaw/Position/Sensor/Value")
            try:
                limits = self.headPitchLimitsAtYaw(headYawPosition)
            except IndexError:
                return False

            if angle > limits[0] and angle < limits[1]:
                return True
                
        elif joint in self.jointLimits.keys():
            if angle > self.jointLimits[joint][0] and angle < self.jointLimits[joint][1]:
                return True
            #else:
                #print(angle)
                #print(self.jointLimits[joint])
        else:
            raise IndexError("Limits for ", joint, " not found.")
        return False



    def stopOnCollision(self, joints, defaultStiffness=0.5, defaultSpeed=0.1):
        """Returns True if current reach given value

        joints -- dictionary with angle, stiffness and name as key
        defaulfStiffness -- 0.3 for normal joint, for WristYaw 0.5"""
        averages={} #dict for moving average of each joint
        last_positions={}
        for joint in joints:
            if "stiffness" in joints[joint]:
                self.motion.setStiffnesses(joint, joints[joint]["stiffness"])
            else:
                self.motion.setStiffnesses(joint, defaultStiffness)
            if "speed" in joints[joint]:
                self.motion.setAngles(joint, joints[joint]["angle"], joints[joint]["speed"])
            else:
                self.motion.setAngles(joint, joints[joint]["angle"], defaultSpeed)
            last_positions[joint]=float(self.memory.getData("Device/SubDeviceList/" + joint + "/Position/Sensor/Value"))
            averages[joint]=[]
        time.sleep(0.25) #time for robot to init the move
        while True:
            over_limit=False
            final_joints=0
            joints_in_collision = 0
            time.sleep(0.1)
            for joint in joints:
                current = float(self.memory.getData("Device/SubDeviceList/" + joint + "/ElectricCurrent/Sensor/Value"))
                if current!=0.0:
                    averages[joint].append(current)
                    average=sum(averages[joint])/len(averages[joint])
                try:
                    average = sum(averages[joint]) / len(averages[joint])
                except:
                    average=0
                position=float(self.memory.getData("Device/SubDeviceList/" + joint + "/Position/Sensor/Value"))
                position_change=abs(last_positions[joint]-position) #Check if joint move
                if current>average+average*0.5 and position_change<0.01: #If position didnt change and current is bigger then moving average + some value
                    joints_in_collision+=1
                #if current>self.currentLimits[joint]:
                    #over_limit=True
                if abs(position-joints[joint]["angle"])<0.2:
                    final_joints+=1
                last_positions[joint]=position
            if final_joints==len(joints): #if target reached
                print("target")
                return False
            if joints_in_collision>2 or over_limit: #if collision occured
                print("Collision")
                for joint in joints:
                    self.motion.changeAngles(joint,0,1)#stop motors
                time.sleep(1)
                return True
if __name__ == "__main__":
    test = safeMotion()
    print("test.checkJointMove(\"HeadYaw\", 0.04)", test.checkJointMove("HeadYaw", 0.04))
    print("test.checkJointMove(\"HeadYaw\", 3)", test.checkJointMove("HeadYaw", 3))
    print("")
    print("test.checkJointMove(\"HeadPitch\", 0.04)", test.checkJointMove("HeadPitch", 0.04))
    print("test.checkJointMove(\"HeadPitch\", 0.1)", test.checkJointMove("HeadPitch", 0.1))
    print("")
    print("test.checkJointMove(\"LShoulderRoll\", 0.04)", test.checkJointMove("LShoulderRoll", 0.04))
    print("test.checkJointMove(\"LShoulderRoll\", 3)", test.checkJointMove("LShoulderRoll", 3))
    #0.58..,1.58...,0.08...
    #-0.04,-1.04
    """
    new_limits={}
    start_position={}
    hand=["LWristYaw","LElbowYaw","LElbowRoll","LShoulderRoll","LShoulderPitch"]


    joint=hand[0]
    new_limits[joint]={}
    for stiffness in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
        print(stiffness)
        test.motion.setStiffnesses(joint,stiffness)
        limit=[[],[]]
        for i in range(10):
            test.motion.setAngles(joint,test.jointLimits[joint][0], 0.2)
            time.sleep(3)
            print("0", test.memory.getData("Device/SubDeviceList/"+joint+"/ElectricCurrent/Sensor/Value"))
            limit[0].append(test.memory.getData("Device/SubDeviceList/"+joint+"/ElectricCurrent/Sensor/Value"))
            test.motion.setAngles(joint, test.jointLimits[joint][1], 0.2)
            t = time.time()
            time.sleep(3)
            print("1",test.memory.getData("Device/SubDeviceList/"+joint+"/ElectricCurrent/Sensor/Value"))
            limit[1].append(test.memory.getData("Device/SubDeviceList/"+joint+"/ElectricCurrent/Sensor/Value"))
        new_limits[joint][stiffness]=limit
    """
    """https://drive.google.com/drive/u/0/my-drive
    limit = {}
    for stiffness in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        limit[stiffness]=[[],[]]
        test.motion.setStiffnesses(joint, stiffness)
        test.motion.setAngles(joint, test.jointLimits[joint][0]+0.5, 0.2)
        for i in range(100):
            limit[stiffness][0].append(test.memory.getData("Device/SubDeviceList/" + joint + "/ElectricCurrent/Sensor/Value"))
    for stiffness in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
            test.motion.setStiffnesses(joint, stiffness)
            test.motion.setAngles(joint, test.jointLimits[joint][1]-0.5, 0.2)
            for i in range(100):
                limit[stiffness][1].append(test.memory.getData("Device/SubDeviceList/" + joint + "/ElectricCurrent/Sensor/Value"))
    new_limits[joint] = limit
    """
    """
    all={}
    for stiffness in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        test.motion.setStiffnesses(joint, stiffness)
        current=[]
        for i in range(10):
            test.motion.setAngles(joint, test.jointLimits[joint][0] + 0.5, 0.2)
            t=time.time()
            while True:
                current.append(test.memory.getData("Device/SubDeviceList/" + joint + "/ElectricCurrent/Sensor/Value"))
                if time.time()-t>1:
                    break
            test.motion.setAngles(joint, test.jointLimits[joint][1] - 0.5, 0.2)
            t = time.time()
            while True:
                current.append(test.memory.getData("Device/SubDeviceList/" + joint + "/ElectricCurrent/Sensor/Value"))
                if time.time() - t > 1:
                    break
        all[stiffness]=current

    with open('/home/rustli/NAO/'+str(joint)+'_average.pickle', 'wb') as handle:  # Save as pickle
        pickle.dump(all, handle, protocol=pickle.HIGHEST_PROTOCOL)
    """
    """

    hand = ["RWristYaw", "RElbowYaw", "RElbowRoll", "RShoulderRoll", "RShoulderPitch"]
    hand_l = ["LWristYaw", "LElbowYaw", "LElbowRoll", "LShoulderRoll", "LShoulderPitch"]
    for joint in hand:
        print(joint,test.memory.getData("Device/SubDeviceList/" + joint + "/Position/Sensor/Value"))
    print("_______________________________________________")
    for joint in hand_l:
        print(joint,test.memory.getData("Device/SubDeviceList/" + joint + "/Position/Sensor/Value"))
    """
    #print("Test",test.stopOnCollision({"RShoulderRoll":{"angle":-0.1396},"RElbowRoll":{"angle":0.1611},"RElbowYaw":{"angle":0.1043},"RWristYaw":{"angle":-1.6491},"RShoulderPitch":{"angle":1.9129}}))
    #joints={"RShoulderRoll": {"angle": -0.1396}, "RElbowRoll": {"angle": 0.1611}, "RElbowYaw": {"angle": 0.1043},
     #"RWristYaw": {"angle": -1.6491}, "RShoulderPitch": {"angle": 1.9129}}
    #for j in joints:
        #self.motion.setStiffnesses(joint, defaultStiffness)
    raw_input()
        #print(test.motion.getAngles("RShoulderPitch",1))
    print("LShoulderPitch",float(test.memory.getData("Device/SubDeviceList/LShoulderPitch/Position/Sensor/Value")))
    print("LShoulderRoll", float(test.memory.getData("Device/SubDeviceList/LShoulderRoll/Position/Sensor/Value")))
    print("LElbowYaw", float(test.memory.getData("Device/SubDeviceList/LElbowYaw/Position/Sensor/Value")))
    print("LElbowRoll", float(test.memory.getData("Device/SubDeviceList/LElbowRoll/Position/Sensor/Value")))
    print("LWristYaw", float(test.memory.getData("Device/SubDeviceList/LWristYaw/Position/Sensor/Value")))
