import rospy
from std_msgs.msg import  Float64
from time import sleep
from std_msgs.msg import Int32
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
import quadrotor_msgs.msg as quadrotor_msgs

"""
user:~$ rosmsg show nav_msgs/Odometry
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
string child_frame_id
geometry_msgs/PoseWithCovariance pose
  geometry_msgs/Pose pose
    geometry_msgs/Point position
      float64 x
      float64 y
      float64 z
    geometry_msgs/Quaternion orientation
      float64 x
      float64 y
      float64 z
      float64 w
  float64[36] covariance
geometry_msgs/TwistWithCovariance twist
  geometry_msgs/Twist twist
    geometry_msgs/Vector3 linear
      float64 x
      float64 y
      float64 z
    geometry_msgs/Vector3 angular
      float64 x
      float64 y
      float64 z
  float64[36] covariance
"""
import numpy as np

def quat_to_euler_angles(q):
    #  Computes the euler angles from a unit quaternion using the
    #  z-y-x convention.
    #  euler_angles = [roll pitch yaw]'
    #  A quaternion is defined as q = [qw qx qy qz]'
    #  where qw is the real part.

    euler_angles = np.zeros((3, 1))

    euler_angles[0] = np.arctan2(
        2*q.w*q.x + 2*q.y*q.z, q.w*q.w - q.x*q.x - q.y*q.y + q.z*q.z)
    euler_angles[1] = -np.arcsin(2*q.x*q.z - 2*q.w*q.y)
    euler_angles[2] = np.arctan2(
        2*q.w*q.z + 2*q.x*q.y, q.w*q.w + q.x*q.x - q.y*q.y - q.z*q.z)
    return euler_angles

_autopilot_feedback = quadrotor_msgs.AutopilotFeedback()

def autopilot_feedback_cb(msg):
    #print(msg.reference_state)
    message_odometry.pose.pose.position.x = msg.reference_state.pose.position.x
    message_odometry.pose.pose.position.y = msg.reference_state.pose.position.y
    message_odometry.pose.pose.position.z = msg.reference_state.pose.position.z
    
    euler = quat_to_euler_angles(msg.reference_state.pose.orientation)
    message_odometry.twist.twist.linear.x = euler[0]
    message_odometry.twist.twist.linear.y = euler[1]
    message_odometry.twist.twist.linear.z = euler[2]

if __name__ == "__main__":
    #rospy.init_node('topic_publisher', log_level=rospy.DEBUG)
    #rospy.init_node('topic_publisher', log_level=rospy.INFO) WARN
    rospy.init_node('state_estimate_topic_publisher', log_level=rospy.INFO)
    # quad_namespace = "/1"
    pub = rospy.Publisher("/test/state_estimate", Odometry, 
                                  queue_size=10)

    pub1 = rospy.Publisher("sbus_bridge/arm", Odometry, 
                                  queue_size=10)
    pub2 = rospy.Publisher("control_command", Odometry, 
                                  queue_size=10)


    _autopilot_feedback_sub = rospy.Subscriber('/test/autopilot/feedback',
            quadrotor_msgs.AutopilotFeedback, autopilot_feedback_cb)

    rate = rospy.Rate(60)

    message_odometry = Odometry()
    message_odometry.header.frame_id = "world"
    print(message_odometry)
    print(type(message_odometry))
    pub.publish(message_odometry)
    while not rospy.is_shutdown():
      print(message_odometry)
      pub.publish(message_odometry)
      rate.sleep()

      # exit()
      # print(message_odometry.twist.twist.linear)
      # print(message_odometry.pose.pose.position)
      # print(_autopilot_feedback.reference_state.velocity.linear)
