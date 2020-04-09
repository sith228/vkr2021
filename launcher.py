import argparse
import logging

from common.logger import init_logger
from common.server import Server


def init_arg_parser():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument("port", type=int, action="store", choices=range(0, 65535), help="Server port number")

    # Optional arguments
    parser.add_argument("-detector", default="default", type=str, action="store", choices=["default"], help="Text detection network")
    parser.add_argument("-recognizer", default="moran",  type=str, action="store", choices=["default", "moran"], help="Text recognition network")
    parser.add_argument("-debug", action="store_true")
    return parser


init_logger()
log = logging.getLogger("root")
log.info("Hello, logger here")

arg_parser = init_arg_parser()
args = arg_parser.parse_args()
log.info("Hello, argparcer here")

s = Server(args)
log.info("Hello, server init successful")
s.run()
