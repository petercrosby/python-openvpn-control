"""
python-openvpn-control
----------

Links
`````
* `Docs <https://github.com/petercrosby/python-openvpn-control>`_
* `GitHub <https://github.com/petercrosby/python-openvpn-control>`_

"""

import os
import sys
import re

from setuptools import setup, find_packages
from setuptools.command.install import install


NAME = "python-openvpn-control"
PACKAGE_NAME = "openvpn_control"
LICENSE = "GPLv3"
PROJECT_URL = "https://github.com/petercrosby/python-openvpn-control"
DESCRIPTION = "Python wrapper of openvpn using subprocess."
AUTHOR_NAME = 'Peter Crosby'
AUTHOR_EMAIL = 'p.crosby25@gmail.com'
KEYWORDS = ("python setuptools openvpn")
MIN_VERSION = (3, 6, 8)
PYTHON_REQUIRES = ">=3.6.8"
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Environment :: Console",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: SQL",
    "Natural Language :: English",
    "Topic :: Database",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Typing :: Typed"
]
PLATFORMS = ["linux", "linux2", "darwin"]

with open(os.path.join(PACKAGE_NAME, "__init__.py"), "rt") as f:
    version = re.search("__version__ = \"([^\"]+)\"", f.read()).group(1)

if sys.version_info < MIN_VERSION:
    print(f'ERROR: {NAME} requires at least Python {MIN_VERSION} to run.')
    sys.exit(1)

# Set the requirements.txt file path, located next to setup.py
requirements_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'requirements.txt')


def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != version:
            info = f"Git tag: {tag} does not match the version of this app: {version}"
            sys.exit(info)


try:
    with open(requirements_file, 'r') as open_file:
        requirements = open_file.readlines()
except (FileNotFoundError, IOError):
    raise

setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=readme(),
    long_description_content_type='text/markdown',
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR_EMAIL,
    license=LICENSE,
    url=PROJECT_URL,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    install_requires=requirements,
    python_requires=PYTHON_REQUIRES,
    platforms=PLATFORMS,
    packages=find_packages(exclude=("tests", "setup")),
    test_suite="tests",
    setup_requires=[
        "wheel", "twine"
    ],
    extras_require={
        'test': [
            'unittests',
            'coverage',
            'codecov'
        ]
    },
    cmdclass={
        "verify": VerifyVersionCommand,
    }
)
