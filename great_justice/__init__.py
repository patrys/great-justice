# -*- coding: utf-8 -*-

import logging
import sys
import traceback

def what_happen():
    logging.debug(u'一体どうしたと言んだ！')
    stack = []
    trace = sys.exc_info()[2]
    while trace:
        stack.append(trace.tb_frame)
        trace = trace.tb_next
    logging.debug(traceback.format_exc())
    for frame in stack:
        logging.debug(u'%s at line %s in %s' % (frame.f_code.co_filename,
                                                frame.f_lineno,
                                                frame.f_code.co_name))
        for key, value in frame.f_locals.items():
            if not key.startswith('_'):
                try:
                    logging.debug(u'\t%20s = %s' % (key, value))
                except:
                    logging.debug(u'\t%20s = <EXCEPTION RAISED WHILE TRYING TO PRINT>' % key)
