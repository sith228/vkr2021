import logging
import os

from flask import Flask, request, Response

from pipelines.bus_detection_pipeline import BusDetectionPipeline
from common.session import Session

class Server:
    def __init__(self, args):
        # setup Flask
        self.__app = Flask(__name__)
        self.__init_flask()
        self.__port = args.port
        self.__debug = args.debug
        self.__log = logging.getLogger("root")
        self.__log.info("Server init complete")
        self.__debug_output_dir = args.output_dir  # TODO: - delete from here
        self.__bus_detection_pipeline = BusDetectionPipeline()
        self.__session = Session(None, None, None, None)
        self.__session.subscribe_to_result(self.callback)

    def callback(self, message):
        pass

    def __init_flask(self):
        """

        Rules for apply get request.

        """
        # Get image handler
        self.__app.add_url_rule('/bus_detection', 'bus_detection', lambda: Response(self.bus_detection()),
                                methods=['GET', 'POST'])

    def bus_detection(self):
        return self.__bus_detection_pipeline.start_processing(request.data)

    def run(self):
        os.makedirs(self.__debug_output_dir, exist_ok=True)
        if os.path.exists(self.__debug_output_dir):
            self.__debug_output_dir = os.path.abspath(self.__debug_output_dir)
            self.__log.info("Save directory created: {}".format(self.__debug_output_dir))
        if self.__debug:
            os.makedirs(self.__debug_output_dir + "/debug", exist_ok=True)
            self.__log.info("Debug save directory created: {}/debug".format(self.__debug_output_dir))
        # TODO: - transfer code behind (37:43)
        self.__app.run(host="0.0.0.0", port=self.__port, threaded=True)
