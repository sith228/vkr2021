import logging
import logging.config


def init_logger():
    logger_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '[%(asctime)s:%(msecs)03d] %(name)s %(levelname)-5s %(message)s',
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
                'filename': "test_summary.log",
                'encoding': 'utf-8',
                'mode': 'w',
                'formatter': 'default'
            },
            'test_log': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': 'test_results.log',
                'encoding': 'utf-8',
                'mode': 'w',
                'formatter': 'default'
            }
        },
        'loggers': {
            'main': {
                'handlers': ['summary', 'console'],
                'level': 'DEBUG',
                'propagate': True
            },
            'tests': {
                'level': 'DEBUG',
                'handlers': ['test_log']
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['console', 'summary']
            },
        },
    }

    logging.config.dictConfig(logger_config)
