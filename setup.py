#!/usr/bin/env python3

import re
from setuptools import setup

with open("ossaudit/__init__.py") as f:
    _src = f.read()

_version = re.search(r'^__version__ = "(.+)"', _src, re.M).group(1)
_project = re.search(r'^__project__ = "(.+)"', _src, re.M).group(1)

setup(
    name=_project,
    version=_version,
    author="Stuart Zurcher",
    author_email="stuartz.ccrx@gmail.com",
    maintainer="Stuart Zurcher",
    maintainer_email="stuartz.ccrx@gmail.com",
    license="BSD-2-Clause",
    description="Audit python packages for known vulnerabilities using Sonatype OSS Index v3 API",  # noqa
    long_description=(
        "Fork of ossaudit by Hans Jerry Illikainen "
        "(https://github.com/illikainen/ossaudit). "
        "Includes some portions of PRs from sseide. "
        "See https://github.com/stuartz/ossaudit"
    ),
    url="https://github.com/stuartz/ossaudit",
    python_requires=">=3.5",
    entry_points={
        "console_scripts": ["ossaudit = ossaudit.__main__:main"],
    },
    packages=[
        "ossaudit",
    ],
    install_requires=[
        "appdirs",
        "click",
        "dparse",
        "requests",
        "texttable",
    ],
    tests_requires=[
        "coverage",
        "isort",
        "mccabe",
        "mypy",
        "pycodestyle",
        "pyflakes",
        "pylint",
        "pylint-quotes",
        "yapf",
    ],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Security",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
)
