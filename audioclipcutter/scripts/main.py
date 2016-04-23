# -*- coding: utf-8 -*-
import sys
import argparse

from audioextractor.audio_extractor import AudioCutter

def cli():
    args = parseArgs(sys.argv[1:])

    print("{}\n{}".format(audioPath, specPath))
    try:
        extr = AudioExtractor(audioPath)
        extr.extractClips(specPath)
    except Exception as e:
        # print(e)
        raise e
        exit(1)

    exit(0)

def parseArgs(args):
    parser = argparse.ArgumentParser(description="Audio Clip Cutter")
    parser.add_argument('--output-dir', '-o', nargs=1, default='')
    parser.add_argument('--zip', '-z', action='store_true')
    parser.add_argument('--labels', '-l', nargs=1)
    parser.add_argument('files', nargs='*')

    return parser.parse_args(args)

def checkIfThereIsDataBeingPipedToStdin():
    import sys
    import os
    from stat import S_ISFIFO

    if S_ISFIFO(os.fstat(0).st_mode):
        return True
    else:
        return False
