# -*- coding: utf-8 -*-

'''
great-justice:

A more useful alternative to regular stack traces.
'''

import contextlib
import inspect
import sys
import traceback

from . import structure
from . import utils

def what_happen(logger=None):
    '''
    Print information about the current stack trace
    '''
    utils.log(logger, structure.WhatHappen())
    exc_type, exc_value, trace = sys.exc_info()
    while trace:
        frame = trace.tb_frame
        trace = trace.tb_next
        filename = inspect.getsourcefile(frame)
        # skip self
        filename_base = filename.rsplit('.', 1)[0]
        local_base = __file__.rsplit('.', 1)[0]
        if filename_base == local_base:
            continue
        utils.log_frame(logger, frame)
    utils.log(
        logger,
        structure.ExceptionValue(
            ''.join(traceback.format_exception(exc_type, exc_value,
                                               trace)).strip()))

@contextlib.contextmanager
def take_your_time(logger=None):
    '''
    Trap errors occuring inside this context processor and print them
    using what_happen
    '''
    try:
        yield
    except Exception: # pylint: disable=W0703
        what_happen(logger=logger)
        raise
