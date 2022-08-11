#! /usr/bin/python
import actionlib
import rospy
from panda_perception.msg import GetBoxPoseAction, GetBoxPoseGoal, GetBoxPoseResult


class BoxBehaviour(object):
    def __init__(self, *args):

        self.center_x = 0
        self.center_y = 0
        self.angle = 0

        self.get_box_pose_client = actionlib.SimpleActionClient(
            "/get_box_pose", GetBoxPoseAction
        )

        print("Waiting for get_box_pose server")
        self.get_box_pose_client.wait_for_server()
        print("Connected to get_box_pose_ server")

    def run(self):
        goal_msg = self.createGetBoxPoseGoalMessage(
            camera_topic="/camera/depth_registered/points",
            transform_to_link="panda_link0",
            min_x=0.1,
            max_x=1.5,
            min_y=-0.5,
            max_y=0.5,
            min_z=0,
            max_z=1.5,
            surface_threshold=0.015,
        )

        self.get_box_pose_client.send_goal_and_wait(goal_msg)
        state = self.get_box_pose_client.get_state()

        if state == actionlib.GoalStatus.SUCCEEDED:
            result = self.get_box_pose_client.get_result()
            self.center_x = result.center_x
            self.center_y = result.center_y
            self.angle = result.angle
        else:
            print("Failed to get box pose")
            self.center_x = 0
            self.center_y = 0
            self.angle = 0
        pass

    def createGetBoxPoseGoalMessage(
        self,
        camera_topic,
        transform_to_link,
        min_x,
        max_x,
        min_y,
        max_y,
        min_z,
        max_z,
        surface_threshold,
    ):
        goal_msg = GetBoxPoseGoal()
        goal_msg.camera_topic = camera_topic
        goal_msg.transform_to_link = transform_to_link
        goal_msg.min_x = min_x
        goal_msg.max_x = max_x
        goal_msg.min_y = min_y
        goal_msg.max_y = max_y
        goal_msg.min_z = min_z
        goal_msg.max_z = max_z
        goal_msg.surface_threshold = surface_threshold

        return goal_msg

    def get_box_pose(self):
        return self.center_x, self.center_y, self.angle
