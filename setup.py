try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='audioclipcutter',
    version='0.1.8',
    description='Easily extract multiple clips from audio files',
    long_description=open('README.rst').read(),
    license='MIT',
    author='Tiago Bras',
    author_email='tiagodsbras@gmail.com',
    download_url='http://tiagobras.com/download',
    url='http://tiagobras.com',
    packages=find_packages(exclude=[]),
    include_package_data=True,
    # package_dir={'': 'src'},
    package_data = {
        # 'audioclipcutter': ['bin/*'],
    },
    install_requires=[
        # 'Click',
        # 'python-helper-utils'
    ],
    dependency_links=[
    #     "git+ssh://git@gitlab.com:TiagoBras/python-helper-utils.git"
        # "../TBUtils"
    ],
    # data_files=[('my_data', ['ffmpeg/ffmpeg', 'ffmpeg/ffmpeg.exe'])],
    # scripts = ["runner"],
    entry_points='''
        [console_scripts]
        audiocutter=audioclipcutter.scripts.main:cli
    ''',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
