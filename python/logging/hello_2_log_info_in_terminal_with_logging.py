#!/usr/bin/env python3

import logging

logging.basicConfig(level=logging.INFO)

logging.debug('A debug message') # This will not print anything as the logging level is now INFO
logging.info('An info message')
logging.warning('Something is not right.')
logging.error('A Major error has happened.')
logging.critical('The entire system is down.')