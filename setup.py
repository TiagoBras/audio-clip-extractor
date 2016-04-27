try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

def version():
    with open('VERSION') as f:
        return f.read().strip()

    raise FileNotFoundError("Error: 'VERSION' file not found.")
    
setup(
    name='audioclipcutter',
    version=version(),
    description='Easily extract multiple clips from audio files',
    long_description=open('README.md').read(),
    license='MIT',
    author='Tiago Bras',
    author_email='tiagodsbras@gmail.com',
    download_url='http://tiagobras.com/download',
    url='http://tiagobras.com',
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
        audioclipcutter=audioclipcutter.scripts.main:cli
    ''',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
