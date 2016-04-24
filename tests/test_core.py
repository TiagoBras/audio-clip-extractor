# -*- coding: utf-8 -*-
import sys
import os
import shutil

sys.path.insert(0, os.path.abspath('..'))

from audioclipcutter.core import AudioClipCutter

TEST_DIR = os.path.abspath("tests/data/")

class TestAudioCutter:
    def assert_exported_clips(self, amountOfClips):
        for i in range(1, amountOfClips+1):
            extratedClipPath = os.path.join(TEST_DIR, "clip%d.mp3" % i)
            expectedClipPath = os.path.join(TEST_DIR, "expected_clip%d.mp3" % i)

            assert os.path.isfile(extratedClipPath)

            f_extracted = open(extratedClipPath, 'rb')
            f_expected = open(expectedClipPath, 'rb')

            # Compare files
            try:
                assert f.read() == f_expected.read(), "'%s' It doesn't match expected data" % expectedClipPath
            except(Exception) as e:
                f_expected.close()
                f_extracted.close()

                os.unlink(extratedClipPath)

            if os.path.isfile(extratedClipPath):
                os.unlink(extratedClipPath)

    def test_audio_extract_using_filepath_m4a_input(self):
        ffmpegPath = shutil.which('ffmpeg.exe' if sys.platform == "win32" else 'ffmpeg')
        extractor = AudioClipCutter('tests/data/synthesized_speech.mp3', ffmpegPath)
        extractor.extractClips('tests/data/synthesized_speech.txt', TEST_DIR)

        self.assert_exported_clips(6)
