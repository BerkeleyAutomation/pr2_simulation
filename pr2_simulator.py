import queuePlanner
import recorder
import roslib
roslib.load_manifest('gazebo_msgs')

import rospy
from gazebo_msgs.srv import DeleteModel
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState

import utils #for teleop

'''EXPLICIT LOCATIONS USED'''
RED = [0.701716, 0.400784, 0.83095]
BLUE = [0.701716, 0.000784, 0.83095]
GREEN = [0.701716, -0.400784, 0.83095]
TARGET_GREEN = [0.6, -0.405, 0.82]
ALIGN_GRASP_GREEN = [0.7, -0.405, 0.82]
RAISED_GREEN = [0.7, -0.405, 1.0]
RAISED_DEST_GREEN = [0.7, 0.0, 1.0]
DEST_GREEN = [0.7, 0.0, 0.83]
DEST_GREEN_REMOVED = [0.45, 0.0, 1.0]

_cylinder_name = "unit_object_Green"
_cylinder_model_state = ModelState()
_cylinder_model_state.model_name = _cylinder_name
_cylinder_model_state.reference_frame = ''

'''OUTPUT FILE TO WRITE TO'''
FILENAME = '/home/simon/experiment'

def delete_cylinder():
  rospy.wait_for_service("/gazebo/delete_model")
  try:
    s = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)
    resp = s(_cylinder_name)
  except rospy.ServiceException, e:
    print "error when calling delete_cylinder: %s"%e
    sys.exit(1)

def reset_cylinder():
  rospy.wait_for_service("/gazebo/set_model_state")
  try:
    s = rospy.ServiceProxy("gazebo/set_model_state", SetModelState)
    print _cylinder_model_state
    resp = s(_cylinder_model_state)
  except rospy.ServiceException, e:
    print "error when calling reset_cylinder: %s"%e
    sys.exit(1)

def save_cylinder_state():
  rospy.wait_for_service("/gazebo/get_model_state")
  try:
    s = rospy.ServiceProxy("gazebo/get_model_state", GetModelState)
    temp = s(_cylinder_name, None)
    _cylinder_model_state.pose = temp.pose
    _cylinder_model_state.twist = temp.twist
  except rospy.ServiceException, e:
    print "error when calling save_cylinder_state: %s"%e
    sys.exit(1)

def teleop():
  char = ''
  while char != 'q':
    char = utils.Getch.getch()
    if char == 'r' or char == 'R':
      print "Reseting Cylinder"
      reset_cylinder()
    elif char == 's' or char == 'S':
      save_cylinder_state()
      print "Saving Cylinder"
    rospy.sleep(.01)



def main():
  save_cylinder_state()
  goalPositions = ["CLEAR", TARGET_GREEN, ALIGN_GRASP_GREEN, "GRASP", RAISED_GREEN, RAISED_DEST_GREEN, DEST_GREEN, "RELEASE", RAISED_DEST_GREEN, DEST_GREEN_REMOVED]
  qPlan = queuePlanner.QueuePlanner()

  for i in xrange(3):
    qPlan.setPositionQueue(goalPositions)
    rec = recorder.Recorder(FILENAME + str(i))
    rec.startRecording()
    qPlan.run()
    rec.stopRecording()
    reset_cylinder()


if __name__ == '__main__':
    main()
