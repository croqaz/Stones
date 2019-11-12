#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://github.com/kennethreitz/setup.py ❤️ ✨ 🍰 ✨

import os
from setuptools import setup, find_packages

NAME = 'stones'
DESCRIPTION = 'Persistent key-value containers, compatible with Python dict.'
KEYWORDS = 'persistent dict'
URL = 'https://github.com/croqaz/Stones'
AUTHOR = 'Cristi Constantin'
EMAIL = 'cristi.constantin@speedpost.net'

here = os.path.abspath(os.path.dirname(__file__))
about = {}

with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

setup(
    version=about['__version__'],
    name=NAME,
    description='Base library for persistent key-value stores, 100% compatible with Python dict',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords=KEYWORDS,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=True,
    python_requires='>= 3.6',
    extras_require={
        'dev': ['flake8', 'codecov'],
        'test': ['pytest', 'pytest-cov'],
    },
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Database',
    ])
