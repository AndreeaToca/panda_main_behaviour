import sys
import rospy

# from the sub-behaviour folder import the BoxEstimationBehaviour class
from sub_behaviours import box_perception_behaviour


class MainBehaviour(object):
    def __init__(self, *args):
        self.box_estimation_behaviour = box_perception_behaviour.BoxBehaviour()
        self.box_perception = True

        self.center_x = 0
        self.center_y = 0
        self.angle = 0
        pass

    def run(self):
        if self.box_perception:
            self.box_estimation_behaviour.run()
            self.box_perception = False
            (
                self.center_x,
                self.center_y,
                self.angle,
            ) = self.box_estimation_behaviour.get_box_pose()
        print(self.center_x, self.center_y, self.angle)
        pass


def main(args):
    rospy.init_node("main_behaviour")
    main_behaviour = MainBehaviour()
    main_behaviour.run()


if __name__ == "__main__":
    main(sys.argv)
