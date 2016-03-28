from os.path import exists
from os import unlink

import pytest

from audioextractor.audio_extractor import AudioExtractor

class TestAudioExtractor:
    def test_audio_extract_using_filepaths(self):
        extractor = AudioExtractor('tests/data/audio_data.m4a')
        extractor.extractClips('tests/data/labels_data.txt')

        assert exists('clip2.mp3')

        for i in range(1, 3):
            extratedClipFilename = 'clip%d.mp3' % i

            assert exists(extratedClipFilename)

            with open('clip%d.mp3' % i, 'rb') as f:
                with open('tests/data/expected_clip%d.mp3' % i, 'rb') as f_expected:
                    assert f.read() == f_expected.read()

            # Delete all the extracted clips since we don't need them anymore
            unlink(extratedClipFilename)
