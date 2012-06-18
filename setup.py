#! /usr/bin/env python
from setuptools import setup, find_packages

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Debuggers',
    'Topic :: Software Development :: Libraries :: Python Modules']

REQUIREMENTS = ['termcolor >= 1.0.0']

setup(name='great-justice',
      author='Patryk Zawadzki',
      author_email='patrys@gmail.com',
      description='Debug every ZIG',
      version = '2012.6.5',
      packages = find_packages(),
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      platforms=['any'],
      zip_safe=True)
