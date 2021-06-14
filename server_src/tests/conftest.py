import atexit

import pytest
from _pytest.runner import runtestprotocol
from tests.metrics.experiment import Experiment
from tests.metrics.writer import Writer
from typing import Mapping, List

EXPERIMENTS = [Experiment('bus_route_performance', 'performance')]
VALUES: Mapping[str, List[float]] = {'bus_route_performance': []}


def pytest_addoption(parser):
    parser.addoption("--benchmark", action='store_true', default=False, help='run benchmark for pipeline bus rout '
                                                                             'number recongnition')


def pytest_configure(config):
    config.addinivalue_line('markers', 'benchmark: run benchmark.')


def pytest_collection_modifyitems(config, items):
    if config.getoption('--benchmark'):
        return
    skip_benchmark_test = pytest.mark.skip(reason='need --benchmark option to run')
    for item in items:
        if 'benchmark' in item.keywords:
            item.add_marker(skip_benchmark_test)

def pytest_runtest_protocol(item, nextitem):
    reports = runtestprotocol(item, nextitem=nextitem)
    for report in reports:
        if report.when == 'call' and (item.name.split('[')[0] == 'test_bus_number_recognition') or item.name.split('[')[0] == 'test_dataset_to_server':
            VALUES['bus_route_performance'].append(report.duration)


@atexit.register
def dump_metrics():
    for experiment in EXPERIMENTS:
        experiment.append(experiment.name, VALUES[experiment.name])
        Writer.write(experiment)
