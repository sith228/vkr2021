import logging
import os

from flask import Flask, request, Response

from response_callbacks.low_res import LowRes


class Server(object):
    def __init__(self, args):
        # setup Flask
        self.app = Flask(__name__)
        self.init_flask()
        self.port = args.port
        self.debug = args.debug
        self.log = logging.getLogger("root")
        self.log.info("Server init complete")
        self.output_dir = args.output_dir
        self.low_res_image_handler = LowRes(args.output_dir, self.debug)

    def init_flask(self):
        """

        Rules for apply get request.

        """
        # Get image handler
        self.app.add_url_rule('/load_low_res_image', 'load_low_res_image',
                              lambda: Response(self.load_low_res_image()),
                              methods=['GET', 'POST'])

    def load_low_res_image(self):
        result = self.low_res_image_handler.startProcessing(request.data)
        return result

    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)
        if os.path.exists(self.output_dir):
            self.output_dir = os.path.abspath(self.output_dir)
            self.log.info("Save directory created: {}".format(self.output_dir))
        if self.debug:
            os.makedirs(self.output_dir + "/debug", exist_ok=True)
            self.log.info("Debug save directory created: {}/debug".format(self.output_dir))

        self.app.run(host="0.0.0.0", port=self.port, threaded=True)
