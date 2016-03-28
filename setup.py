try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='AudioClipExtractor',
    version='0.1.1',
    description='Easily extract multiple clips from audio files',
    long_description=open('README.txt').read(),
    author='Tiago Bras',
    author_email='tiagodsbras@gmail.com',
    download_url='http://tiagobras.com/download',
    url='http://tiagobras.com',
    packages=['audioextractor', ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
