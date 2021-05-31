import atexit
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter
import os

from io import BytesIO
from threading import Lock

from . import Experiment


# TODO: Create temp folder automatically
class Writer:
    __mutex: Lock = Lock()
    __workbook: xlsxwriter.Workbook = xlsxwriter.Workbook('metrics.xlsx')

    @classmethod
    def write(cls, experiment: Experiment):
        """
        Writes experiment to output file
        :param experiment: Experiment that should be written
        :return: Nothing
        """
        cls.__mutex.acquire()
        os.makedirs('./temp', exist_ok=True)
        worksheet = cls.__workbook.add_worksheet(experiment.name)
        for i, value in enumerate(experiment.values.items()):
            worksheet.write(0, i, value[0])
            worksheet.write_column(1, i, value[1])
            if experiment.model == 'accuracy':
                # cls.__add_accuracy_plot(worksheet, value)
                cls.test(worksheet, value)

                pass

            if experiment.model == 'performance':
                cls.test(worksheet, value)
                pass
                # cls.__add_accuracy_plot(worksheet, value)

        cls.__mutex.release()

    @classmethod
    def test(cls, worksheet, value):
        lst = range(len(value[1]))
        plt.plot(lst, value[1])
        plt.xlabel(value[0])
        os.makedirs(os.path.dirname('log/'), exist_ok=True)
        image_path = './temp/plot_{}.png'.format(value[0])
        plt.savefig(image_path)
        image_data = BytesIO(open(image_path, 'rb').read())
        worksheet.insert_image('C2', image_path, {'image_data': image_data})
        plt.close()

    @classmethod
    def __add_accuracy_plot(cls, worksheet, value):
        plt.hist(value[1], density=True)
        plt.xlabel(value[0])
        image_path = './temp/plot_{}.png'.format(value[0])
        plt.savefig(image_path)
        image_data = BytesIO(open(image_path, 'rb').read())
        worksheet.insert_image('C2', image_path, {'image_data': image_data})
        plt.close()

    @classmethod
    def close(cls):
        """
        Closes output file
        :return: Nothing
        """
        cls.__workbook.close()
        raise RuntimeError('This method should be executed only automatically')


@atexit.register
def save():
    try:
        Writer.close()
    except RuntimeError:
        pass

