#!/usr/bin/env python3

import logging

logging.debug('A debug message')  # This will not print anything as by default the logging level is WARNING
logging.info('An info message')   # This will not print anything as by default the logging level is WARNING
logging.warning('Something is not right.')
logging.error('A Major error has happened.')
logging.critical('The entire system is down.')