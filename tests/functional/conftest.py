import atexit

from _pytest.runner import runtestprotocol
from tests.metrics.experiment import Experiment
from tests.metrics.writer import Writer
from typing import Mapping, List

experiments = [Experiment('bus_route_performance', 'performance')]
VALUES: Mapping[str, List[float]] = {'bus_route_performance': []}


def pytest_runtest_protocol(item, nextitem):
    reports = runtestprotocol(item, nextitem=nextitem)
    for report in reports:
        if report.when == 'call' and item.name.split('[')[0] == 'test_bus_number_recognition':
            VALUES['bus_route_performance'].append(report.duration)


@atexit.register
def dump_metrics():
    for experiment in experiments:
        experiment.append(experiment.name, VALUES[experiment.name])
        Writer.write(experiment)
