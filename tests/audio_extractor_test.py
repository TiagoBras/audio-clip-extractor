# -*- coding: utf-8 -*-
from os.path import exists, join
from os import unlink

import pytest

from audioextractor.audio_extractor import AudioExtractor

TESTS_DIR = "tests/data/"

class TestAudioExtractor:
    def assert_exported_clips(self, amountOfClips):
        for i in range(1, amountOfClips+1):
            extratedClipPath = join(TESTS_DIR, "clip%d.mp3" % i)
            expectedClipPath = join(TESTS_DIR, "expected_clip%d.mp3" % i)

            assert exists(extratedClipPath)

            f_extracted = open(extratedClipPath, 'rb')
            f_expected = open(expectedClipPath, 'rb')

            # Compare files
            try:
                assert f.read() == f_expected.read(), "'%s' It doesn't match expected data" % expectedClipPath
            except(Exception) as e:
                f_expected.close()
                f_extracted.close()

                unlink(extratedClipPath)

            if exists(extratedClipPath):
                unlink(extratedClipPath)

    def test_audio_extract_using_filepath_m4a_input(self):
        extractor = AudioExtractor('tests/data/synthesized_speech.mp3')
        extractor.extractClips('tests/data/synthesized_speech.txt', TESTS_DIR)

        self.assert_exported_clips(6)
