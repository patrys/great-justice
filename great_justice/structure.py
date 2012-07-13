# -*- coding: utf-8 -*-

'''
Basic structured for the printer
'''

from termcolor import colored


class Structure(object):
    '''
    Basic structure for formatting output
    '''
    # pylint: disable=R0903
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
    # pylint: disable=R0903
    attrs = {'color': 'red'}
    args = [u'一体どうしたと言んだ！']

    def __init__(self):
        # pylint: disable=W0231
        pass


class VariableName(Structure):
    '''
    A variable's name
    '''
    # pylint: disable=R0903
    attrs = {'color': 'yellow'}


class Value(Structure):
    '''
    A variable's value
    '''
    # pylint: disable=R0903
    attrs = {'color': 'green'}


class Duration(Structure):
    '''
    A time span
    '''
    # pylint: disable=R0903
    attrs = {'color': 'white', 'attrs': ['dark']}

class UndefinedValue(Structure):
    '''
    An undefined value
    '''
    # pylint: disable=R0903
    attrs = {'color': 'red'}


class ShortVariable(Structure):
    '''
    A single-line variable
    '''
    # pylint: disable=R0903
    def __init__(self, variable_name, variable_value):
        # pylint: disable=W0231
        self.args = [VariableName(variable_name),
                     u' = ',
                     Value(variable_value)]


class LongVariable(Structure):
    '''
    A multi-line variable
    '''
    # pylint: disable=R0903
    def __init__(self, variable_name):
        # pylint: disable=W0231
        self.args = [VariableName(variable_name),
                     u' = \\']


class UndefinedVariable(Structure):
    '''
    A variable we could not determine value of
    '''
    # pylint: disable=R0903
    def __init__(self, variable_name):
        # pylint: disable=W0231
        self.args = [VariableName(variable_name),
                     u' = ',
                     UndefinedValue(u'<undefined>')]


class CurrentLine(Structure):
    '''
    The highlighted line of code
    '''
    # pylint: disable=R0903
    attrs = {'color': 'white'}


class CodeLine(Structure):
    '''
    The regular lines
    '''
    # pylint: disable=R0903
    attrs = {'color': 'white', 'attrs': ['dark']}


class Code(Structure):
    '''
    A piece of code
    '''
    # pylint: disable=R0903
    def __init__(self, prefix, line, suffix):
        self.args = []
        for pl in prefix:
            self.args.append(u'  ')
            self.args.append(CodeLine(pl))
            self.args.append(u'\n')
        self.args.append(u'→ ')
        self.args.append(CurrentLine(line))
        for sl in suffix:
            self.args.append(u'\n')
            self.args.append(u'  ')
            self.args.append(CodeLine(sl))


class CodeFileName(Structure):
    '''
    A filename
    '''
    # pylint: disable=R0903
    attrs = {'attrs': ['bold']}


class CodeScope(Structure):
    '''
    A scope name (function, <module> etc.)
    '''
    # pylint: disable=R0903
    attrs = {'attrs': ['bold']}


class FileReference(Structure):
    '''
    A code reference
    '''
    # pylint: disable=R0903
    def __init__(self, filename, line_no, scope):
        # pylint: disable=W0231
        self.args = [u'File "',
                     CodeFileName(filename),
                     u'", line ',
                     CodeLineNo(line_no),
                     u', in ',
                     CodeScope(scope)]


class CodeLineNo(Structure):
    '''
    A line no. in code reference
    '''
    # pylint: disable=R0903
    attrs = {'attrs': ['bold']}


class ExceptionValue(Structure):
    '''
    The exception
    '''
    # pylint: disable=R0903
    attrs = {'color': 'red', 'attrs': ['reverse']}


class CallArguments(Structure):
    '''
    List of call parameters
    '''
    # pylint: disable=R0903
    def __init__(self, arguments):
        # pylint: disable=W0231
        pairs = [[VariableName(key), '=', Value(val)]
                 for key, val in sorted(arguments.iteritems())]
        self.args = reduce(lambda a, b: a + [u', '] + b, pairs)


class Call(Structure):
    '''
    A value is being returned
    '''
    # pylint: disable=R0903
    def __init__(self, name, params):
        # pylint: disable=W0231
        self.args = [VariableName(name),
                     u'(',
                     CallArguments(params),
                     u')…']

class CallReturn(Structure):
    '''
    A value is being returned
    '''
    # pylint: disable=R0903
    def __init__(self, value, duration):
        # pylint: disable=W0231
        self.args = [u'… = ', Value(value), ' ', Duration(duration)]
