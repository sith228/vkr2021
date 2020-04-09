import logging
import os

from flask import Flask, request, Response

from response_callbacks.high_res import HighRes
from response_callbacks.high_res_color import HighResColor
from response_callbacks.low_res import LowRes
from response_callbacks.low_res_color import LowResColor


class Server(object):
    def __init__(self, args, log):
        # setup Flask
        self.app = Flask(__name__)
        self.init_flask()
        self.port = args.port
        self.debug = args.debug
        self.log = logging.getLogger("root")
        self.log.info("Server init complete")
        self.output_dir = None
        self.low_res_image_handler = LowRes()
        self.low_res_color_image_handler = LowResColor()
        self.high_res_image_handler = HighRes()
        self.high_res_color_image_handler = HighResColor()

    def init_flask(self):
        """

        Rules for apply get request.

        """
        # Get image handler
        self.app.add_url_rule('/load_low_res_image', 'load_low_res_image',
                              lambda: Response(self.load_low_res_image()),
                              methods=['GET', 'POST'])
        self.app.add_url_rule('/load_low_res_color_image', 'load_low_res_color_image',
                              lambda: Response(self.load_low_res_color_image()),
                              methods=['GET', 'POST'])
        self.app.add_url_rule('/load_high_res_image', 'load_high_res_image',
                              lambda: Response(self.load_high_res_image()),
                              methods=['GET', 'POST'])
        self.app.add_url_rule('/load_high_res_color_image', 'load_high_res_color_image',
                              lambda: Response(self.load_high_res_color_image()),
                              methods=['GET', 'POST'])

    def load_low_res_image(self):
        result = self.low_res_image_handler.startProcessing(request.data)
        return result

    def load_low_res_color_image(self):
        pass

    def load_high_res_image(self):
        pass

    def load_high_res_color_image(self):
        pass

    def run(self):
        output_dir = os.path.join("files")
        os.makedirs(output_dir, exist_ok=True)
        if os.path.exists(output_dir):
            self.output_dir = os.path.abspath(output_dir)
            self.log.info("Save directory created: {}".format(self.output_dir))
        if self.debug:
            os.makedirs(self.output_dir + "/debug", exist_ok=True)
            self.log.info("Debug save directory created: {}/debug".format(self.output_dir))

        self.app.run(host="0.0.0.0", port=self.port, threaded=True)
