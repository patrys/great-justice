# -*- coding: utf-8 -*-

'''
Helper utils
'''

import ast
import linecache
import textwrap

def get_code(filename, lineno, module_globals):
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
