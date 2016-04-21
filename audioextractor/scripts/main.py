# -*- coding: utf-8 -*-
import sys

from audioextractor.audio_extractor import AudioExtractor

def cli():
    audioPath = sys.argv[1]
    specPath = sys.argv[2]
    print("{}\n{}".format(audioPath, specPath))
    try:
        extr = AudioExtractor(audioPath)
        extr.extractClips(specPath)
    except Exception as e:
        # print(e)
        raise e
        exit(1)

    exit(0)
