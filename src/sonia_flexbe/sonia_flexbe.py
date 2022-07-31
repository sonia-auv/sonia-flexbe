#! /usr/bin/env python3
from http.client import NotConnected
import os
import rospy
import rospkg

from flexbe_msgs.msg import BehaviorExecutionActionGoal
from std_msgs.msg import Empty
from std_msgs.msg import String
from xml.dom import minidom
from std_srvs.srv import Trigger, TriggerResponse

class SoniaFlexbe:

    def __init__(self):
        rospy.init_node('sonia_flexbe')

        self.current_mission = None

        # Get manifest folder
        rp = rospkg.RosPack()
        self.missions_directory = os.path.join(rp.get_path('sonia_flexbe_behaviors'), 'manifest')

        # Subscribers
        self.mission_name_sub = rospy.Subscriber('/sonia_flexbe/mission_name_msg', String, self.handle_current_mission)
        
        # Publishers
        self.flexbe_behavior_pub = rospy.Publisher('/flexbe/execute_behavior/goal', BehaviorExecutionActionGoal, queue_size=5)
        self.flexbe_preempt_pub = rospy.Publisher('/flexbe/command/preempt', Empty, queue_size=100)

        # Services
        rospy.Service('/sonia_flexbe/list_missions', Trigger, self.handle_list_missions)

        rospy.spin()
    
    # Handler to get start the mission loaded by the telemetry.
    # - req: Requested mission name.
    # - return: 
    def handle_current_mission(self, req):
        rospy.loginfo("Mission selected : {}".format(req.data))
        self.current_mission = req.data
        msg = BehaviorExecutionActionGoal()
        msg.goal.behavior_name = self.current_mission
        self.flexbe_behavior_pub.publish(msg)
        

    # Handler to list every available missions
    # - req: Parameter not used.
    # - return: Mission list as a service response.
    def handle_list_missions(self, req):
        rospy.loginfo("List mission")
        missions_list = ""
        for file in os.listdir(self.missions_directory):
            mission_file = minidom.parse(os.path.join(self.missions_directory, file))
            mission = mission_file.getElementsByTagName('behavior')
            mission_name = mission[0].attributes['name'].value
            missions_list = missions_list + mission_name + ";"
        return TriggerResponse(success=True, message = missions_list)

if __name__ == '__main__':
    SoniaFlexbe()