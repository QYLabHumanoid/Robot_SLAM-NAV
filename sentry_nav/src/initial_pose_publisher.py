#!/usr/bin/env python3
import rospy
import tf2_ros
from geometry_msgs.msg import PoseWithCovarianceStamped, TransformStamped

def publish_initial_pose():
    rospy.init_node('initial_pose_publisher', anonymous=True)
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)
    pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)

    rate = rospy.Rate(10)  # 发布频率 10 Hz
    while not rospy.is_shutdown():
        try:
            # 获取 base_link 在 map 中的位置
            transform: TransformStamped = tf_buffer.lookup_transform("map", "base_link", rospy.Time(0))
            initial_pose = PoseWithCovarianceStamped()
            initial_pose.header.stamp = rospy.Time.now()
            initial_pose.header.frame_id = "map"
            initial_pose.pose.pose.position.x = transform.transform.translation.x
            initial_pose.pose.pose.position.y = transform.transform.translation.y
            initial_pose.pose.pose.position.z = 0.0
            initial_pose.pose.pose.orientation = transform.transform.rotation
            initial_pose.pose.covariance = [0.0] * 36  # 可调整为合适的协方差
            pub.publish(initial_pose)
        except Exception as e:
            rospy.logwarn(f"Could not get transform: {e}")
        rate.sleep()

if __name__ == "__main__":
    try:
        publish_initial_pose()
    except rospy.ROSInterruptException:
        pass
