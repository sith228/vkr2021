import logging
import logging.config
import os


class Filter(logging.Filter):
    def filter(self, record):
        if record.name == 'root':
            return True
        elif record.name == 'pipelines':
            return True
        elif record.name == 'test_pipelines':
            return True
        return False


class Logger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name)
        self.addFilter(Filter())


def init_logger():
    logger_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '[%(asctime)s:%(msecs)03d] [%(levelname)5s] [%(name)10s]  %(message)s',
                'datefmt': '%d.%m %H:%M:%S',
            }, 'net': {
                'format': '%(asctime)s %(message)s',
                'datefmt': '%m-%d %H:%M:%S',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'summary': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': "log/test_summary.log",
                'encoding': 'utf-8',
                'mode': 'w',
                'formatter': 'default'
            },
        },
        'loggers': {
            'main': {
                'handlers': ['summary', 'console'],
                'level': 'DEBUG',
                'propagate': True
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['console', 'summary'],
            },
            'pipelines': {
                'level': 'DEBUG',
                'handlers': ['summary'],
            },
        },
    }
    os.makedirs(os.path.dirname('log/'), exist_ok=True)
    logging.setLoggerClass(Logger)
    logging.config.dictConfig(logger_config)


def init_logger_test():
    logger_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '[%(asctime)s:%(msecs)03d] [%(levelname)5s] [%(name)10s] %(message)s',
                'datefmt': '%d.%m %H:%M:%S',
            }
        },
        'handlers': {
            'results': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': 'log/pipeline_results.log',
                'encoding': 'utf-8',
                'mode': 'a',
                'formatter': 'default'
            }
        },
        'loggers': {
            'test_pipelines': {
                'level': 'INFO',
                'handlers': ['results'],
            }
        },
    }
    os.makedirs(os.path.dirname('log/'), exist_ok=True)
    logging.setLoggerClass(Logger)
    logging.config.dictConfig(logger_config)
