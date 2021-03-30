import os
import sys

from openvino.inference_engine import IENetwork, IEPlugin
import numpy as np

from common.utils.os_utils import OsUtil


class InferenceEngine(object):
    def __init__(self, xml_path: str, bin_path: str, width: int = 0, height: int = 0, device: str = "CPU",
                 cpu_extension: str = ""):
        """

        :param xml_path:
        :param bin_path:
        :param width:
        :param height:
        :param device:
        :param cpu_extension: Path to cpu extensions
        """
        print('Loading IR to the plugin...')  # TODO: Use logs
        self.model_xml = xml_path
        self.model_bin = bin_path
        self.device = device
        if cpu_extension == "":
            extension_folder = os.path.abspath(os.path.join("tools", "InferenceEngine"))
            if OsUtil.is_windows():
                self.cpu_extension = os.path.join(extension_folder, "cpu_extension.dll")
                if not os.listdir(extension_folder):
                    self.cpu_extension = os.path.join("\\Program Files (x86)\\IntelSWTools\\openvino",
                                                      "inference_engine\\bin\\intel64\\Release",
                                                      "cpu_extension.dll")
            elif OsUtil.is_macos():
                self.cpu_extension = os.path.join(extension_folder, "libcpu_extension.dylib")
                if not os.listdir(extension_folder):
                    self.cpu_extension = os.path.join("/opt/intel/openvino/inference_engine/lib/intel64",
                                                      "libcpu_extension.dylib")
            else:
                self.cpu_extension = os.path.join(extension_folder, "libcpu_extension.so")
                if not os.listdir(extension_folder):
                    self.cpu_extension = os.path.join("/opt/intel/openvino/inference_engine/lib/intel64/Release",
                                                      "libcpu_extension_avx2.so")
        else:
            self.cpu_extension = cpu_extension
        self.plugin = IEPlugin(device=device, plugin_dirs="")
        if self.cpu_extension and 'CPU' in self.device:
            if os.path.exists(self.cpu_extension):
                self.plugin.add_cpu_extension(self.cpu_extension)
            else:
                print("Warning: CPU EXTENSION NOT FOUND") # TODO: Use logs
        self.net = IENetwork(model=xml_path, weights=bin_path)

        if width != 0 or height != 0:
            inputs = self.net.inputs
            n, c, h, w = self.net.inputs['Placeholder'].shape
            inputs['Placeholder'] = (n, c, height, width)
            self.net.reshape(inputs)

        self.exec_net = self.plugin.load(network=self.net, num_requests=2)

    def inference_sync(self, frame: np.ndarray):
        """
        Starts net
        :param frame: Input image
        :return: Net output tensor
        """
        # input_image = frame
        print('Starting inference...')
        if len(frame.shape) == 3:
            frame = frame.transpose((2, 0, 1))
        # else:
        #     input_image = input_image.transpose(0, 1))
        n, c, h, w = self.net.inputs['Placeholder'].shape
        frame = frame.reshape((n, c, h, w)).astype(np.float32)

        # Run the net.
        outputs = self.exec_net.infer({'Placeholder': frame})
        if len(self.net.outputs.keys()) > 1:
            result = [outputs[k] for k in self.net.outputs.keys()]
            result.sort(key=lambda x: x.shape[1])
            return result
        return outputs[next(iter(self.net.outputs.keys()))]
