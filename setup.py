try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='AudioClipExtractor',
    version='0.1.4',
    description='Easily extract multiple clips from audio files',
    long_description=open('README.rst').read(),
    author='Tiago Bras',
    author_email='tiagodsbras@gmail.com',
    download_url='http://tiagobras.com/download',
    url='http://tiagobras.com',
    packages=find_packages(exclude=[]),
    # package_dir={'': 'src'},
    package_data = {
        'audioextractor': ['bin/*'],
    },
    install_requires=[
        'Click',
    ],
    # data_files=[('my_data', ['ffmpeg/ffmpeg', 'ffmpeg/ffmpeg.exe'])],
    # scripts = ["runner"],
    entry_points='''
        [console_scripts]
        audiocutter=audioextrator.scripts.main:cli
    ''',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
