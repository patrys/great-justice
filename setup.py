#! /usr/bin/env python
from setuptools import setup, find_packages

version = __import__('great_justice').get_version()

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
    'Topic :: Software Development :: Libraries :: Python Modules',
]

PACKAGE_DATA = {}

REQUIREMENTS = [
    'django >= 1.3',
]

EXTRAS = {}

setup(name='great-justice',
      author='Patryk Zawadzki',
      author_email='patrys@gmail.com',
      description='Debug every ZIG',
      version = version,
      packages = find_packages(),
      package_data=PACKAGE_DATA,
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      extras_require=EXTRAS,
      platforms=['any'],
      zip_safe=True)
