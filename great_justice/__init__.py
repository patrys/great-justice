# -*- coding: utf-8 -*-

import contextlib
import linecache
import logging
import re
import sys

VERSION = (2011, 9, 0, 'final', 0)
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

LOGGER = logging.getLogger('CATS')

def what_happen():
    LOGGER.debug(u'一体どうしたと言んだ！')
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
        LOGGER.debug(u'  File "%s", line %s, in %s' % (filename,
                                                      frame.f_lineno,
                                                      frame.f_code.co_name))
        linecache.checkcache(filename)
        line = linecache.getline(filename, frame.f_lineno, frame.f_globals)
        if line:
            line = line.strip()
            LOGGER.debug(u'    %s' % (line, ))
            tokens = IDENTIFIER_RE.split(line)
            for key, value in frame.f_locals.items():
                if key in tokens:
                    try:
                        LOGGER.debug(u'      %s = %s' % (key, repr(value)))
                    except:
                        LOGGER.debug(u'      %s = <EXCEPTION RAISED WHILE TRYING TO PRINT>' % key)
    LOGGER.debug(u'      %s' % (exc_value, ))

@contextlib.contextmanager
def take_your_time():
    try:
        yield
    except:
        what_happen()
        raise
