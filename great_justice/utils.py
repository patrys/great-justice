# -*- coding: utf-8 -*-

'''
Helper utils
'''

import inspect
import linecache
import pprint

from . import structure

def get_source(obj):
    '''
    Get the source code for the frame object
    '''
    filename = inspect.getsourcefile(obj)
    linecache.checkcache(filename)
    lineno = inspect.getlineno(obj)
    prefix = [(linecache.getline(filename, ln) or u'~').strip('\r\n')
              for ln in range(lineno-3, lineno)]
    current = linecache.getline(filename, lineno).strip('\r\n')
    suffix = [(linecache.getline(filename, ln) or u'~').strip('\r\n')
              for ln in range(lineno+1, lineno+4)]
    return prefix, current, suffix

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
        structure.FileReference(filename, frame.f_lineno, frame.f_code.co_name),
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
    prefix, line, suffix = get_source(frame)
    missing = object()
    if line:
        log(logger, structure.Code(prefix, line, suffix), indent=indent+1)
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
