import os
from setuptools import setup, find_packages

# package meta info
NAME = "CodeCLI"
VERSION = "1.0"
DESCRIPTION = "A command line tool for github"
AUTHOR = "Qiangning Hong"
AUTHOR_EMAIL = "hongqn@gmail.com"
LICENSE = "BSD"
URL = ""
KEYWORDS = ""
CLASSIFIERS = []

# package contents
MODULES = []
PACKAGES = find_packages(exclude=[
    'tests.*', 'tests', 'examples.*', 'examples'])
ENTRY_POINTS = """
[console_scripts]
code = codecli:main
"""

# dependencies
INSTALL_REQUIRES = [
    "six",
]
SETUP_REQUIRES = [
    'pytest-runner',
]
TESTS_REQUIRE = [
    'nose',
]

here = os.path.abspath(os.path.dirname(__file__))


def read_long_description(filename):
    path = os.path.join(here, filename)
    if os.path.exists(path):
        return open(path).read()
    return ""

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read_long_description('README.rst'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    py_modules=MODULES,
    packages=PACKAGES,
    install_package_data=True,
    zip_safe=False,
    entry_points=ENTRY_POINTS,
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    tests_require=TESTS_REQUIRE,
)
