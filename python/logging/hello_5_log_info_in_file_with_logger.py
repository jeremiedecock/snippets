#!/usr/bin/env python3

import logging

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='log_info_in_file_logger.log', level=logging.INFO)

    logger.info('Hello')
    logger.info('World')

if __name__ == '__main__':
    main()