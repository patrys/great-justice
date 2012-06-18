# -*- coding: utf-8 -*-

import contextlib
import linecache
import os
import pprint
import re
import sys
import textwrap
import traceback

from termcolor import colored

VERSION = (2012, 6, 0, 'final', 0)
IDENTIFIER_RE = re.compile('\W')

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

    attrs = {}

    def __init__(self, value):
        self.args = [value]

    def __unicode__(self):
        return u''.join(unicode(arg) for arg in self.args)

    def prettyformat(self):
        return colored(
            u''.join(arg.prettyformat()
            if isinstance(arg, Structure) else unicode(arg)
            for arg in self.args), **self.attrs)


class WhatHappen(Structure):

    attrs = {'color': 'red'}
    args = [u'一体どうしたと言んだ！']

    def __init__(self):
        pass


class VariableName(Structure):

    attrs = {'color': 'yellow'}


class VariableValue(Structure):

    attrs = {'color': 'green'}


class ShortVariable(Structure):

    def __init__(self, variable_name, variable_value):
        self.args = [VariableName(variable_name),
                     ' = ',
                     VariableValue(variable_value)]


class LongVariable(Structure):

    def __init__(self, variable_name):
        self.args = [VariableName(variable_name),
                     ' = \\']


class Code(Structure):

    attrs = {'attrs': ['bold']}


class CodeFileName(Structure):

    attrs = {'attrs': ['bold']}


class CodeLine(Structure):

    def __init__(self, filename, line_no, object_name):
        self.args = [u'File "',
                     CodeFileName(filename),
                     u'", line ',
                     CodeLineNo(line_no),
                     u', in ',
                     CodeObjectName(object_name)]


class CodeLineNo(Structure):

    attrs = {'attrs': ['bold']}


class CodeObjectName(Structure):

    attrs = {'attrs': ['bold']}


class ExceptionValue(Structure):

    attrs = {'color': 'red', 'attrs': ['reverse']}


def what_happen(logger=None):
    def log(info, indent=0):
        if logger:
            lines = unicode(info).splitlines()
            for line in lines:
                logger.debug('  ' * indent + line)
        else:
            lines = info.prettyformat().splitlines()
            for line in lines:
                print '  ' * indent + line
    def get_code(filename, lineno, module_globals):
        linecache.checkcache(filename)
        code = linecache.getline(filename, lineno, module_globals)
        if code:
            without_comments = code.split('#', 1)[0]
            while without_comments.count(')') > without_comments.count('('):
                lineno -= 1
                prev_line = linecache.getline(filename, lineno, module_globals)
                code = prev_line + code
                without_comments = prev_line.strip().split('#', 1)[0] + '\n' + without_comments
            return textwrap.dedent(code)

    log(WhatHappen())
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
        log(struct)
        line = get_code(filename, frame.f_lineno, frame.f_globals)
        
        if line:
            line = line.strip()
            tokens = IDENTIFIER_RE.split(line)
            log(Code(line), indent=1)
            for key, value in frame.f_locals.items():
                if key in tokens:
                    try:
                        value = pprint.pformat(value, width=60)
                    except Exception:
                        log(
                            ShortVariable(
                                key,
                                '<EXCEPTION RAISED WHILE TRYING TO PRINT>'),
                            indent=2)
                    else:
                        if value.count('\n'):
                            log(LongVariable(key), indent=2)
                            log(VariableValue(value), indent=3)
                        else:
                            log(ShortVariable(key, value), indent=2)
    log(
        ExceptionValue(
            ''.join(traceback.format_exception(exc_type, exc_value,
                                               trace)).strip()))

@contextlib.contextmanager
def take_your_time(logger=None):
    try:
        yield
    except:
        what_happen(logger=logger)
        raise
