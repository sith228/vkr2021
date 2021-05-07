import argparse
import logging

from common.logger import init_logger
from server.tcpserver import TCPServer


class Launcher(object):
    def __init__(self):
        args = self.__get_argument_parser().parse_args()
        self.server = TCPServer('', args.port)
        logger.info("Server initialized")

    @staticmethod
    def __get_argument_parser() -> argparse.ArgumentParser:
        """
        Returns argument parser
        :return: argument parser
        """

        parser = argparse.ArgumentParser()
        # Required arguments
        parser.add_argument("port", type=int, action="store", choices=range(0, 65535), help="Server port number")
        # Optional arguments
        parser.add_argument("-detector", default="default", type=str, action="store", choices=["default"],
                            help="Text detection network")
        parser.add_argument("-recognizer", default="moran", type=str, action="store", choices=["default", "moran"],
                            help="Text recognition network")
        parser.add_argument("-debug", action="store_true")
        parser.add_argument("-output_dir", default="files")
        return parser

    def run(self):
        """
        Starts the server
        """

        self.server.run()


if __name__ == "__main__":
    init_logger()
    logger = logging.getLogger("root")
    logger.info("Logger initialized")

    launch = Launcher()
    launch.run()
