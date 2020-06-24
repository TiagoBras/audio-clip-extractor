try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

import os


def version():
    with open(os.path.abspath('VERSION')) as f:
        return f.read().strip()

    raise IOError("Error: 'VERSION' file not found.")


VERSION = version()

setup(
    name='audioclipextractor',
    version=VERSION,
    description='Easily extract multiple clips from audio files',
    long_description=open(os.path.abspath('README.md')).read(),
    long_description_content_type='text/markdown',
    license='MIT',
    author='Tiago Bras',
    author_email='tiagodsbras@gmail.com',
    download_url='https://github.com/TiagoBras/audio-clip-extractor/tarball/v%s' % VERSION,
    url='https://github.com/TiagoBras/audio-clip-extractor',
    packages=find_packages(exclude=[]),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
        'Topic :: Utilities'
    ],
    entry_points='''
        [console_scripts]
        ace=audioclipextractor.scripts.main:cli
    ''',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
