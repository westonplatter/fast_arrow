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
    packages=['fast_arrow'],
    # install_requires=[
    #     'click',
    #     'Robinhood==1.0.1',
    # ],
    # dependency_links=[
    #     # # this git commit hash is master as of July 14th. It's 64 commits ahead of release 1.0.1
    #     # 'https://github.com/Jamonek/Robinhood/archive/d21b1907dfa0ec9ba04177e597350b7d2a1ef31e.zip#egg=Robinhood-1.0.1',
    #
    #     'https://github.com/westonplatter/Robinhood/archive/6294a5c3d53dd7553c05c272ebeb069df1c86aa2.zip#egg=Robinhood-1.0.1',
    # ],
    entry_points='''
        [console_scripts]
        fa=fast_arrow.cli:cli
    ''',
)
