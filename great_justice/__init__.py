# -*- coding: utf-8 -*-

import contextlib
import linecache
import logging
import os
import re
import sys

VERSION = (2012, 4, 0, 'final', 0)
IDENTIFIER_RE = re.compile('\W')

logger = logging.getLogger('CATS')

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    return version


class Structure(object):

    start_tag = ''
    end_tag = '\033[0m'

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        inner = ''.join(str(arg) for arg in self.args)
        if self.is_interactive():
            return '%s%s%s' % (self.start_tag, inner, self.end_tag)
        return inner

    def is_interactive(self):
        return all(os.isatty(handler.stream.fileno())
                   if hasattr(handler, 'stream') else False
                   for handler in logger.handlers)


class VariableName(Structure):

    start_tag = '\033[95m'

    def __init__(self, variable_name):
        self.args = [variable_name]


class VariableValue(Structure):

    start_tag = '\033[95m'

    def __init__(self, variable_value):
        self.args = [variable_value]


class Variable(Structure):

    def __init__(self, variable_name, variable_value):
        self.args = ['      ', VariableName(variable_name), ' = ',
                     VariableValue(variable_value)]


class CodeFileName(Structure):

    start_tag = '\033[92m'

    def __init__(self, filename):
        self.args = [filename]


class CodeLineNo(Structure):

    start_tag = '\033[92m'

    def __init__(self, line_no):
        self.args = [line_no]


class CodeObjectName(Structure):

    start_tag = '\033[92m'

    def __init__(self, object_name):
        self.args = [object_name]


class CodeLine(Structure):

    def __init__(self, filename, line_no, object_name):
        self.args = ['  File "', CodeFileName(filename), '", line ',
                     CodeLineNo(line_no), ', in ', CodeObjectName(object_name)]


def what_happen():
    logger.debug(u'一体どうしたと言んだ！')
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
        struct = CodeLine(filename, frame.f_lineno, frame.f_code.co_name)
        logger.debug(struct)
        linecache.checkcache(filename)
        line = linecache.getline(filename, frame.f_lineno, frame.f_globals)
        if line:
            line = line.strip()
            logger.debug(u'    %s' % (line, ))
            tokens = IDENTIFIER_RE.split(line)
            for key, value in frame.f_locals.items():
                if key in tokens:
                    try:
                        structure = Variable(key, repr(value))
                    except Exception:
                        structure = Variable(key, '<EXCEPTION RAISED WHILE TRYING TO PRINT>')
                    logger.debug(structure)
    logger.debug(u'      %s' % (exc_value, ))

@contextlib.contextmanager
def take_your_time():
    try:
        yield
    except:
        what_happen()
        raise
