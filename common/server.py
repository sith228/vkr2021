import logging
import os

from flask import Flask, request, Response

from pipelines.bus_route_number_detection_pipeline import BusDetectionPipeline


class Server(object):
    def __init__(self, args):
        # setup Flask
        self.__app = Flask(__name__)
        self.__init_flask()
        self.__port = args.port
        self.__debug = args.debug
        self.__log = logging.getLogger("root")
        self.__log.info("Server init complete")
        self.__debug_output_dir = args.output_dir  # TODO: - delete from here
        self.__low_res_image_handler = BusDetectionPipeline(args.output_dir, self.__debug)

    def __init_flask(self):
        """

        Rules for apply get request.

        """
        # Get image handler
        self.__app.add_url_rule('/load_low_res_image', 'load_low_res_image',
                                lambda: Response(self.load_low_res_image()),
                                methods=['GET', 'POST'])  # TODO: Change url name

    def load_low_res_image(self):
        result = self.__low_res_image_handler.start_processing(request.data)
        return result

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
