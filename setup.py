from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='fast_arrow',
    version='0.0.1',
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
    entry_points='''
        [console_scripts]
        fa=fast_arrow.cli:cli
    ''',
    project_urls={
        'Issue Tracker': 'https://github.com/westonplatter/fast_arrow/issues',
        'Source Code': 'https://github.com/westonplatter/fast_arrow',
    }
)
