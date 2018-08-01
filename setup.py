import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = '-n auto'

    def run_tests(self):
        import shlex
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)



with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='fast_arrow',
    version='0.0.2',
    description='API client for Robinhood',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Weston Platter',
    author_email='westonplatter@gmail.com',
    url='https://github.com/westonplatter/fast_arrow/',
    license='MIT License',
    python_requires=">=3.4",
    packages=['fast_arrow'],
    install_requires=[
        'click',
        'requests',
    ],
    tests_require=[
        'pytest',
        'vcrpy'
    ],
    cmdclass={'test': PyTest},
    entry_points='''
        [console_scripts]
        fa=fast_arrow.cli:cli
    ''',
    project_urls={
        'Issue Tracker': 'https://github.com/westonplatter/fast_arrow/issues',
        'Source Code': 'https://github.com/westonplatter/fast_arrow',
    }
)
