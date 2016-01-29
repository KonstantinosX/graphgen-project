#!/usr/bin/env python
# setup
# Setup script for graphgenpy
#
# Author:   Konstantinos Xirogiannopoulos <kostasx@cs.umd.edu>
# Created:  Sun Jul 20 11:06:56 2014 -0400
#
# Copyright (C) 2015-2016 Konstantinos Xirogiannopoulos
#
# ID: setup.py [] kostasx@cs.umd.edu $

"""
Setup script for graphgenpy
"""

##########################################################################
## Imports
##########################################################################

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\"."
                      "Please install the setuptools package.")

##########################################################################
## Package Information
##########################################################################

# version  = __import__('graphgen').__version__

## Discover the packages
packages = find_packages(where=".", exclude=("examples", "build", "dist", "lib", "temp","TESTS"))

## Load the requirements
requires = []
with open('requirements.txt', 'r') as reqfile:
    for line in reqfile:
        requires.append(line.strip())

## Define the classifiers
classifiers = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
)

## Define the keywords
keywords = ('graphgen','graph','extraction','analytics','relational','database')

## Define the description
long_description = "GraphGen is a blah blah graphs on RDBMSs"

## Define the configuration
config = {
    "name": "graphgenpy",
    "version": 0.6,
    "description": "A wrapper for the GraphGen project",
    "long_description": long_description,
    "license": "MIT",
    "author": "Konstantinos Xirogiannopoulos",
    "author_email": "kostasx@cs.umd.edu",
    "url": "https://cs.umd.edu/~kostasx",
    "packages": packages,
    "classifiers": classifiers,
    "keywords": keywords,
    "install_requires": requires,
    "zip_safe": False,
    "scripts": [],
    "package_data": {'graphgenpy': ['lib/GraphGen-0.0.6-SNAPSHOT-jar-with-dependencies.jar']}
    }

##########################################################################
## Run setup script
##########################################################################

if __name__ == '__main__':
    setup(**config)
