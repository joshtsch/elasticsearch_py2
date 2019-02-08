#!/usr/bin/env python

from setuptools import setup

setup(
    name='elasticsearchpy2',
    version='1.0.0',
    author='Josh Tscheschlog',
    author_email='joshtsch106@gmail.com',
    keywords = "elastic search python2 python",
    url='https://github.com/joshtsch/elasticsearchpy2',
    packages=['elasticsearchpy2'],
    include_package_data=True,
    zip_safe=False,
    tests_require=['nose'],
    test_suite='nose.collector',
)
