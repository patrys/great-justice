# -*- coding: utf-8 -*-

'''
great-justice:

A more useful alternative to regular stack traces.
'''

import contextlib
import pprint
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
        filename = frame.f_code.co_filename
        # skip self
        filename_base = filename.rsplit('.', 1)[0]
        local_base = __file__.rsplit('.', 1)[0]
        if filename_base == local_base:
            continue
        utils.log(logger,
             structure.CodeLine(filename, frame.f_lineno, frame.f_code.co_name))
        line, tokens = utils.get_code(filename, frame.f_lineno, frame.f_globals)
        if line:
            utils.log(logger, structure.Code(line), indent=1)
            for key in tokens:
                value = (frame.f_locals.get(key) or
                         frame.f_globals.get(key) or
                         frame.f_builtins.get(key))
                if value:
                    try:
                        value = pprint.pformat(value, width=60)
                    except Exception: # pylint: disable=W0703
                        utils.log(
                            logger,
                            structure.ShortVariable(
                                key,
                                '<EXCEPTION RAISED WHILE TRYING TO PRINT>'),
                            indent=2)
                    else:
                        if value.count('\n'):
                            utils.log(logger, structure.LongVariable(key),
                                      indent=2)
                            utils.log(logger, structure.Value(value), indent=3)
                        else:
                            utils.log(logger,
                                 structure.ShortVariable(key, value), indent=2)
                else:
                    utils.log(logger, structure.UndefinedVariable(key),
                              indent=2)
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
