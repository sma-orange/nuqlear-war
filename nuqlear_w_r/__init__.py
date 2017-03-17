# -*- coding: utf-8 -*-
"""New Universal Queue - A tool to test DSTK things"""
import logging.config
import os
import json

__author__ = """Ben Smith"""
__email__ = 'ben.smith@orange.com'
__version__ = '0.5.3'
__name__ = 'NuQleaR'

logging_config_file = 'logging.json'

print(logging_config_file)

if os.path.exists(logging_config_file):
    with open(logging_config_file, 'rt') as f:
        config = json.load(f)
        logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    print(logger.name)
else:
    print('No logging, except print()s!')
