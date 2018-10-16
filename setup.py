#!/usr/bin/python

from setuptools import setup

setup(
   name='msgapp',
   version='1.0',
   description='Simple message verification app',
   author='Suresh Dharavath',
   author_email='sureshdh514@gmail.com',
   packages=['msgapp'],
   scripts=[
            'scripts/msgapp',
           ]
)

