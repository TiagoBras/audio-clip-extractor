# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import sys
import argparse
import shutil
import os

from audioclipextractor import AudioClipExtractor

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SETUP_PATH = os.path.join(ROOT_DIR, 'setup.py')

def cli():
    run(sys.argv[1:])

def run(args):
    ffmpegFilename = 'ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg'

    parser = argparse.ArgumentParser(description='''
        This utility allows one to cut multiple clips 
        from a single or multiple audio files.
        ''')
    parser.add_argument('--version', '-V', action='store_true', 
        help='Print the version of the script')
    parser.add_argument('--ffmpeg', default='', 
        help='Specify the FFMPEG executable path')
    parser.add_argument('--output-dir', '-o', default='', 
        help='Set the output directory')
    parser.add_argument('--zip', '-z', action='store_true', 
        help='Archive the output in a zip container')
    parser.add_argument('--skip-path-lookup', action='store_true')
    parser.add_argument('--text-name', '-m', default='m_text', 
        help='Specify the name of the embedded text variable')
    parser.add_argument('files', nargs='*')

    r = parser.parse_args(args)

    if r.version:
        print("AudioClipExtractor %s" % version())
        sys.exit(0)


    # If the ffmpeg executable provided doesn't exist, look elsewhere (PATH)
    if not os.path.isfile(r.ffmpeg):
        if not r.skip_path_lookup:
            r.ffmpeg = which(ffmpegFilename)

        if not r.ffmpeg:
            print("`%s` not found." % ffmpegFilename, file=sys.stderr)
            displayDownloadPage()
            sys.exit(1)

    files = None

    # If there's data being piped to stdin, consume it instead of processing r.files
    if checkIfThereIsDataBeingPipedToStdin():
        files = [os.path.abspath(f.strip()) for f in sys.stdin]
    else:
        files = r.files

    # Extract the clips
    for f in files:
        extractClips(os.path.abspath(f), r.ffmpeg, r.output_dir, r.zip, r.text_name)

    # Show help message when no files are provided
    if not files:
        print("Error: No audio files to process.", file=sys.stderr)
        parser.print_help()
        sys.exit(2)

def extractClips(filepath, ffmpeg, outputDir, zipOutput, textVar):
    specsFile = "%s.txt" % os.path.splitext(filepath)[0]

    if not os.path.isfile(specsFile):
        print("Error: `%s` not found." % specsFile, file=sys.stderr)
        exit(3)

    acc = AudioClipExtractor(filepath, ffmpeg)
    acc.textVar = textVar
    acc.extractClips(specsFile, outputDir, zipOutput)

def checkIfThereIsDataBeingPipedToStdin():
    import sys
    import os
    from stat import S_ISFIFO

    if S_ISFIFO(os.fstat(0).st_mode):
        return True
    else:
        return False

def displayDownloadPage():
    message = 'FFMPEG can be downloaded at '

    if sys.platform == 'linux' or sys.platform == 'linux2':
        message += 'https://ffmpeg.org/download.html#build-linux'
    elif sys.platform ==  'darwin':
        message += 'http://evermeet.cx/ffmpeg/'
    elif sys.platform == 'win32':
        message += 'https://ffmpeg.zeranoe.com/builds/'

    print(message)

def version(directory=ROOT_DIR):
    with open(os.path.join(directory, 'VERSION')) as f:
        return f.read().strip()

    raise IOError("Error: 'VERSION' file not found.")


def which(filename):
    if sys.version_info >= (3,3):
        return shutil.which(filename)
    else:
        for d in os.getenv('PATH').split(os.path.pathsep):
            path = os.path.join(d, filename)
            if os.path.isfile(path):
                return path

        return None
