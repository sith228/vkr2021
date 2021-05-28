import atexit

import cv2
import pytest
import logging
import numpy as np
from typing import List, Mapping

from common.logger import init_logger_test
from tests.checkers.test_checker import Accuracy
from tools.models.object_detector import ObjectDetectorFactory
from tools.models.text_detector import TextDetectorFactory
from tools.models.text_recognizer import TextRecognizerFactory
from tests.metrics.experiment import Experiment
from tests.metrics.writer import Writer

experiments = [Experiment('bus_route_number_recog', 'accuracy')]
VALUES: Mapping[str, List[float]] = {'bus_route_number_recog': []}
IMAGES = Accuracy.get_test_image_text('./tests/checkers/dataset_test')


class TestComplexDataset:

    @pytest.fixture
    def name_complex_data(self):
        return './tests/checkers/dataset_test'

    @pytest.fixture(scope='module')
    def get_class_by_route(self):
        all_names = Accuracy.get_test_image_text('./tests/checkers/dataset_test')
        flows = set()
        for name in all_names:

            flows.add(' '.join(name[0].partition('.j')[0].split(' ')[:-1]).split('/')[-1])
        for flow in flows:
            experiments.append(Experiment(flow, 'accuracy'))
            VALUES[flow] = []
        logging.info('RUN CLASS')

    @pytest.fixture(scope='session')
    def dump_metrics(self):
        for experiment in experiments:
            if len(VALUES[experiment.name]) == 0:
                continue
            experiment.append(experiment.name, VALUES[experiment.name])
            Writer.write(experiment)

    @pytest.mark.skip
    @pytest.mark.usefixtures('get_class_by_route', 'dump_metrics')
    @pytest.mark.parametrize('image_tuple', IMAGES)
    def test_bus_number_recognition(self, name_complex_data, image_tuple):
        init_logger_test()
        logger = logging.getLogger('test_pipelines')
        bus_detector = ObjectDetectorFactory.get('yolo')
        text_recognizer = TextRecognizerFactory.get('moran')
        text_detector = TextDetectorFactory.get('craft')
        logger.info('IMAGE: ' + image_tuple[0])
        image = cv2.imread(image_tuple[0])
        bus_detector.prediction(image)
        bus_boxes = bus_detector.get_boxes()

        for bus_box in bus_boxes:
            logger.info('BOX DETECTED: ' + str(bus_box.get_bound_box()))
            text_detector.prediction(bus_box.get_cropped_image())
            route_number_boxes = text_detector.get_boxes()
            bus_box.insert_boxes(route_number_boxes)
            if len(route_number_boxes) > 0:
                logger.info('HAS TEXT')
            for route_number_box in route_number_boxes:
                text_recognizer.prediction(route_number_box.get_cropped_image())
                route_number_box.text = text_recognizer.get_result()
                logger.info('ROUT RECOG: ' + route_number_box.text)

            data_accur = Accuracy.check_text_box((image_tuple[0], route_number_boxes), name_complex_data, is_intersection=False)[
                    1]
            VALUES['bus_route_number_recog'].append(data_accur)
            name = ' '.join(image_tuple[0].partition('.j')[0].split(' ')[:-1]).split('/')[-1]
            VALUES[name].append(data_accur)

