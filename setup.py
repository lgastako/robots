#!/usr/bin/env python

import setuptools  # for side-effects to make 'python setup.py develop' work
from setuptools import setup


if __name__ == "__main__":
    setup(name="robots",
          version="0.0.1",
          description="Robots.txt Management for Humans",
          author="John Evans",
          author_email="lgastako@gmail.com",
          url="https://github.com/lgastako/robots",
          provides=["robots"],
          modules=["robots"],
          classifiers=["Development Status :: 4 - Beta",
                       "Intended Audience :: Developers",
                       "License :: OSI Approved :: MIT License",
                       "Operating System :: OS Independent",
                       "Programming Language :: Python :: 2",
                       "Environment :: Web Environment",
                       "Topic :: Software Development :: Libraries"])
