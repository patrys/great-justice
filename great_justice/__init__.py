# -*- coding: utf-8 -*-

'''
great-justice:

A more useful alternative to regular stack traces.
'''

import ast
import contextlib
import linecache
import pprint
import sys
import textwrap
import traceback

from termcolor import colored

VERSION = (2012, 6, 2, 'final', 0)

def get_version():
    '''
    Returns module version
    '''
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
    '''
    Basic structure for formatting output
    '''
    attrs = {}

    def __init__(self, value):
        self.args = [value]

    def __unicode__(self):
        return u''.join(unicode(arg) for arg in self.args)

    def prettyformat(self):
        '''
        The colorful version of __unicode__
        '''
        return colored(
            u''.join(arg.prettyformat()
            if isinstance(arg, Structure) else unicode(arg)
            for arg in self.args), **self.attrs)


class WhatHappen(Structure):
    '''
    The welcome message
    '''
    attrs = {'color': 'red'}
    args = [u'一体どうしたと言んだ！']

    def __init__(self):
        # pylint: disable=W0231
        pass


class VariableName(Structure):
    '''
    A variable's name
    '''
    attrs = {'color': 'yellow'}


class Value(Structure):
    '''
    A variable's value
    '''
    attrs = {'color': 'green'}


class UndefinedValue(Structure):
    '''
    An undefined value
    '''
    attrs = {'color': 'red'}


class ShortVariable(Structure):
    '''
    A single-line variable
    '''
    def __init__(self, variable_name, variable_value):
        # pylint: disable=W0231
        self.args = [VariableName(variable_name),
                     ' = ',
                     Value(variable_value)]


class LongVariable(Structure):
    '''
    A multi-line variable
    '''
    def __init__(self, variable_name):
        # pylint: disable=W0231
        self.args = [VariableName(variable_name),
                     ' = \\']


class UndefinedVariable(Structure):
    '''
    A variable we could not determine value of
    '''
    def __init__(self, variable_name):
        # pylint: disable=W0231
        self.args = [VariableName(variable_name),
                     ' = ',
                     UndefinedValue('<undefined>')]


class Code(Structure):
    '''
    A piece of code
    '''
    attrs = {'attrs': ['bold']}


class CodeFileName(Structure):
    '''
    A filename
    '''
    attrs = {'attrs': ['bold']}


class CodeLine(Structure):
    '''
    A code reference
    '''
    def __init__(self, filename, line_no, object_name):
        # pylint: disable=W0231
        self.args = [u'File "',
                     CodeFileName(filename),
                     u'", line ',
                     CodeLineNo(line_no),
                     u', in ',
                     CodeObjectName(object_name)]


class CodeLineNo(Structure):
    '''
    A line no. in code reference
    '''
    attrs = {'attrs': ['bold']}


class CodeObjectName(Structure):
    '''
    A context in code reference
    '''
    attrs = {'attrs': ['bold']}


class ExceptionValue(Structure):
    '''
    The exception
    '''
    attrs = {'color': 'red', 'attrs': ['reverse']}


def _get_code(filename, lineno, module_globals):
    '''
    Instead of providing the last line of a multi-line expression,
    try to provide a valid context by looking for a smallest chunk
    of code that can be compiled
    '''
    linecache.checkcache(filename)
    code = linecache.getline(filename, lineno, module_globals)
    if not code:
        return None, []
    tree = None
    tokens = []
    lines = 0
    while True:
        try:
            tree = ast.parse(textwrap.dedent(code) + '\n')
        except SyntaxError:
            if not lineno or lines > 10:
                break
            lines += 1
            prev_line = linecache.getline(filename, lineno - lines,
                                          module_globals)
            code = prev_line + code
        else:
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    tokens.append(node.id)
            break
    return textwrap.dedent(code.strip()), tokens

def _log(logger, info, indent=0):
    '''
    Either log a clean version of info or print its colorful version
    if no logger is provided
    '''
    if logger:
        lines = unicode(info).splitlines()
        for line in lines:
            logger.debug('  ' * indent + line)
    else:
        lines = info.prettyformat().splitlines()
        for line in lines:
            print '  ' * indent + line

def what_happen(logger=None):
    '''
    Print information about the current stack trace
    '''
    _log(logger, WhatHappen())
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
        _log(logger, CodeLine(filename, frame.f_lineno, frame.f_code.co_name))
        line, tokens = _get_code(filename, frame.f_lineno, frame.f_globals)
        if line:
            _log(logger, Code(line), indent=1)
            for key in tokens:
                value = (frame.f_locals.get(key) or
                         frame.f_globals.get(key) or
                         frame.f_builtins.get(key))
                if value:
                    try:
                        value = pprint.pformat(value, width=60)
                    except Exception: # pylint: disable=W0703
                        _log(
                            logger,
                            ShortVariable(
                                key,
                                '<EXCEPTION RAISED WHILE TRYING TO PRINT>'),
                            indent=2)
                    else:
                        if value.count('\n'):
                            _log(logger, LongVariable(key), indent=2)
                            _log(logger, Value(value), indent=3)
                        else:
                            _log(logger, ShortVariable(key, value), indent=2)
                else:
                    _log(logger, UndefinedVariable(key), indent=2)
    _log(
        logger,
        ExceptionValue(
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
