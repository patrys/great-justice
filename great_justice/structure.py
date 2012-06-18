# -*- coding: utf-8 -*-

'''
Basic structured for the printer
'''

from termcolor import colored


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
