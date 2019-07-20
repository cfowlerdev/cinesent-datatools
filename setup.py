# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encodings='utf-8') as f:
    long_description = f.read()

setup(
    name='datatools',
    version='0.0.1',
    description='Tools for data cleaning and preparation for analysis',
    long_description=long_description,
    long_description_content_type='text/markdown'
    author='Christian Fowler',
    url='https://github.com/cfowlerdev/cinesent-datatools',
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=2.7,<4'
)
