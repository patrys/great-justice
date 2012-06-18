# -*- coding: utf-8 -*-

'''
Helper utils
'''

import ast
import inspect
import linecache
import pprint
import textwrap

from . import structure

def get_module_context(obj):
    '''
    Instead of providing the whole module source, try to provide a valid
    context by looking for a smallest chunk of code that can be compiled
    '''
    filename = inspect.getsourcefile(obj)
    linecache.checkcache(filename)
    lineno = inspect.getlineno(obj)
    code = linecache.getline(filename, lineno, obj.f_globals)
    lines = 0
    while True:
        try:
            ast.parse(textwrap.dedent(code) + '\n')
        except SyntaxError:
            if not lineno or lines > 10:
                return code
            lines += 1
            prev_line = linecache.getline(filename, lineno - lines,
                                          obj.f_globals)
            code = prev_line + code
        else:
            return textwrap.dedent(code.strip('\n\r'))

def get_source(obj):
    '''
    Get the source code for the frame object
    '''
    lines, lineno = inspect.findsource(obj)
    if inspect.isframe(obj) and obj.f_globals is obj.f_locals:
        return get_module_context(obj)
    return textwrap.dedent(
        ''.join(inspect.getblock(lines[lineno:])).strip('\n\r'))

def log(logger, info, indent=0):
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

def log_call(logger, frame, indent=0):
    '''
    Displays the filename and line no.
    '''
    filename = inspect.getsourcefile(frame)
    log(logger,
        structure.CodeLine(filename, frame.f_lineno),
        indent=indent)

def log_invocation(logger, frame, indent=0):
    '''
    Displays the filename, line no. and the function being called
    along with its params
    '''
    log_call(logger, frame, indent=indent)
    arguments = dict(
        (key, pprint.pformat(
            frame.f_locals.get(key, frame.f_globals.get(key))))
        for key in frame.f_code.co_varnames)
    log(logger,
        structure.Call(frame.f_code.co_name, arguments),
        indent=indent)

def log_frame(logger, frame, indent=0):
    '''
    Parse and log a single frame of a traceback
    '''
    log_call(logger, frame, indent=indent)
    code = get_source(frame)
    missing = object()
    if code:
        log(logger, structure.Code(code), indent=indent+1)
        for key in sorted(frame.f_code.co_varnames):
            value = frame.f_locals.get(
                key,
                frame.f_globals.get(
                     key,
                     frame.f_builtins.get(key, missing)))
            if value is not missing:
                try:
                    value = pprint.pformat(value, width=60)
                except Exception: # pylint: disable=W0703
                    log(logger,
                        structure.ShortVariable(
                            key,
                            '<EXCEPTION RAISED WHILE TRYING TO PRINT>'),
                        indent=indent+2)
                else:
                    if value.count('\n'):
                        log(logger, structure.LongVariable(key),
                            indent=indent+2)
                        log(logger, structure.Value(value), indent=indent+3)
                    else:
                        log(logger, structure.ShortVariable(key, value),
                            indent=indent+2)
            else:
                log(logger, structure.UndefinedVariable(key), indent=indent+2)
