# -*- coding: utf-8 -*
#
# ePoint WebShop
# Copyright (C) 2012 ePoint Systems Ltd
# Author: Andrey Martyanov
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import logging

def setup_logger(name):
    """Return preconfigured logger instance"""

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s')
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    return logger