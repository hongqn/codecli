from setuptools import setup

setup(
    name = "CodeCLI",
    version = "0.1",
    description = "Command line interface for code.dapps.douban.com",
    packages = ['codecli'],
    entry_points = {
        'console_scripts': [
            'code = codecli:main',
        ],
    },
)
