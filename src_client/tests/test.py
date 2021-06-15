import rospy;rospy.init_node("aw")
from autopilot_cli import AutopilotWidget as aw
import os
from flask import Flask, request, Response
import json

class Server:
    def __init__(self):
        # setup Flask
        self.__app = Flask(__name__)
        self.__init_flask()
        self.__port = 5000
        self.__debug = False
        self.controls = {"t": 0, "y": 0, "r": 0, "p": 0, "arm": False }
        self.a = aw()
        print("AW")
        self.a.connect('')
        print("CN")
        
    def publish(self):
        data = json.loads(request.data.decode("utf-8"))
        print(data)
        if self.controls['arm'] != data['arm']:
            if data['arm']:
                self.a.on_button_arm_bridge_clicked()
            else: 
                self.a.on_button_disarm_bridge_clicked()
                
        self.controls = data
        self.a.on_publish_control(self.controls['t'], self.controls['r'], 
                                  self.controls['p'], self.controls['y'])
        
        print(self.controls)
        return "{'code': 200}"

    def __init_flask(self):
        """

        Rules for apply get request.

        """
        # Get image handler
        self.__app.add_url_rule('/control', 'control', lambda: Response(self.publish()),
                                methods=['GET', 'POST'])

    def run(self):
        self.__app.run(host='0.0.0.0', port=self.__port, threaded=True)

s = Server()
s.run()