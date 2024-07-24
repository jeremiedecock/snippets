#!/usr/bin/env python3

import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the minimum logging level

# Create a file handler
file_handler = logging.FileHandler('hello_6_log_info_in_terminal_and_file_with_logger_using_prefix.log')
file_handler.setLevel(logging.INFO)

# Create a stream handler (for the terminal)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Log messages
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')