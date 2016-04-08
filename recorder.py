#!/usr/bin/env python
#test client for joint_states_listener

import roslib
roslib.load_manifest('joint_states_listener')
import rospy
from joint_states_listener.srv import ReturnJointStates
import time
import sys
import threading

def call_return_joint_states(joint_names):
    rospy.wait_for_service("return_joint_states")
    try:
        s = rospy.ServiceProxy("return_joint_states", ReturnJointStates)
        resp = s(joint_names)
    except rospy.ServiceException, e:
        print "error when calling return_joint_states: %s"%e
        sys.exit(1)
    for (ind, joint_name) in enumerate(joint_names):
        if(not resp.found[ind]):
            print "joint %s not found!"%joint_name
    return (resp.position, resp.velocity, resp.effort)


#pretty-print list to string
def pplist(list):
    return ' '.join(['%2.3f'%x for x in list])

def record_Right_Arm_Event(verbose, event, filename, joint_names):

    f = open(filename, 'w')
    i = 0
    while(1):
        if i > 10:
            if event.is_set():
                f.close()
                print "File Succesfully Closed"
                return
            else:
                i = 0
        (position, velocity, effort) = call_return_joint_states(joint_names)
        f.write(str(pplist(position)) + '\n')
        if verbose:
            print "position:", pplist(position)
            print "velocity:", pplist(velocity)
            print "effort:", pplist(effort)
        time.sleep(0.1)
        i += 1

def record_Right_Arm(verbose=False):
    joint_names = ["r_shoulder_pan_joint",
                   "r_shoulder_lift_joint",
                    "r_upper_arm_roll_joint",
                    "r_elbow_flex_joint",
                    "r_forearm_roll_joint",
                    "r_wrist_flex_joint",
                    "r_wrist_roll_joint",
                    "r_gripper_joint"]

    f = open('/home/simon/joint_states_out', 'w')
    while(1):
        (position, velocity, effort) = call_return_joint_states(joint_names)
        f.write(str(pplist(position)) + '\n')
        if verbose:
            print "position:", pplist(position)
            print "velocity:", pplist(velocity)
            print "effort:", pplist(effort)
        time.sleep(0.1)

class Recorder():
    '''
    Class for recording the joint states of PR2
    '''
    RIGHT_JOINT_NAMES = ["r_shoulder_pan_joint",
                   "r_shoulder_lift_joint",
                    "r_upper_arm_roll_joint",
                    "r_elbow_flex_joint",
                    "r_forearm_roll_joint",
                    "r_wrist_flex_joint",
                    "r_wrist_roll_joint",
                    "r_gripper_joint"]

    def __init__(self, filename, verbose=False, joint_names = None):
        if joint_names is None:
            self.joint_names = set(self.RIGHT_JOINT_NAMES)
        else:
            self.joint_names = joint_names
        self.filename = filename
        self.verbose = verbose
        self.e = None
        self.thread = None


    def setVerbose(self, bool):
        self.verbose = bool;

    def addJointNames(self, names):
        self.joint_names = self.joint_names + set(names)


    # def remove_joint_names():

    # def clear_joint_name():

    # def add_joint_names_right():

    # def add_joint_names_left():

    def startRecording(self):
        self.e = threading.Event()
        self.e.clear()
        self.thread = threading.Thread(target = record_Right_Arm_Event, args = (self.verbose,self.e, self.filename, self.joint_names))
        self.thread.start()

    def stopRecording(self):
        self.e.set()
        self.thread.join()


#print out the positions, velocities, and efforts of the right arm joints
if __name__ == "__main__":
    record_Right_Arm(True)