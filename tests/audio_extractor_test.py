from os.path import exists
from os import unlink

import pytest

from audioextractor.audio_extractor import AudioExtractor

class TestAudioExtractor:
    def assert_exported_clips(self, amountOfClips, ext):
        for i in range(1, amountOfClips+1):
            extratedClipFilename = 'clip%d.mp3' % i

            assert exists(extratedClipFilename)

            try:
                with open(extratedClipFilename, 'rb') as f:
                    with open('tests/data/%s_expected_clip%d.mp3' % (ext, i), 'rb') as f_expected:
                        assert f.read() == f_expected.read(), "It doesn't match expected data"
            except (AssertionError, FileNotFoundError) as e:
                # Delete remain files
                for j in range(i, amountOfClips+1):
                    extratedClipFilename = 'clip%d.mp3' % j
                    unlink(extratedClipFilename)

                assert 0, str(e)

            # Delete extracted clip since we don't need it anymore
            unlink(extratedClipFilename)

    def test_audio_extract_using_filepath_m4a_input(self):
        extractor = AudioExtractor('tests/data/input_audio_data.m4a')
        extractor.extractClips('tests/data/labels_data.txt')

        self.assert_exported_clips(2, 'm4a')

    def test_audio_extract_using_filepath_mp3_input(self):
        extractor = AudioExtractor('tests/data/input_audio_data.mp3')
        extractor.extractClips('tests/data/labels_data.txt')

        self.assert_exported_clips(2, 'mp3')
