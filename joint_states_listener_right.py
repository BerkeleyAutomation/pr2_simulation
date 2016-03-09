#!/usr/bin/env python
#test client for joint_states_listener

import roslib
roslib.load_manifest('joint_states_listener')
import rospy
from joint_states_listener.srv import ReturnJointStates
import time
import sys
# import threading

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

def record_Right_Arm_Event(verbose, event, filename):
    joint_names = ["r_shoulder_pan_joint",
                   "r_shoulder_lift_joint",
                    "r_upper_arm_roll_joint",
                    "r_elbow_flex_joint",
                    "r_forearm_roll_joint",
                    "r_wrist_flex_joint",
                    "r_wrist_roll_joint",
                    "r_gripper_joint"]

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


#print out the positions, velocities, and efforts of the right arm joints
if __name__ == "__main__":
    record_Right_Arm(True)