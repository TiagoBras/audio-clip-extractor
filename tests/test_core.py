# -*- coding: utf-8 -*-
import sys
import os
import shutil

import constants

sys.path.insert(0, constants.ROOT_DIR)

from audioclipextractor.core import AudioClipExtractor

def findFileRecursively(filename, directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f == filename:
                return os.path.join(root, f)

    return None

def joinDataDir(filename):
    return os.path.join(constants.TESTS_DATA_DIR, filename)

class TestAudioClipExtractor:
    def setup_class(self):
        filename = 'ffmpeg.exe' if sys.platform == "win32" else 'ffmpeg'

        # First: looks for the executable recursively in ROOT_DIR
        ffmpegPath = findFileRecursively(filename, constants.ROOT_DIR)

        if not ffmpegPath:
            # Second: looks for the executable in PATH
            ffmpegPath = shutil.which(filename)

        self.ffmpegPath = ffmpegPath
        self.audioPath = os.path.join(constants.TESTS_DATA_DIR, 'synthesized_speech.mp3')
        self.specsPath = os.path.join(constants.TESTS_DATA_DIR, 'synthesized_speech.txt')
        self.LABELS_SAMPLE = """
        0.303745	0.861787	A saga de um vaqueiro
        1.570524	2.618325	Brincar de amar
        2.818466	4.292451	A praia
        4.731815	9.730024	Menino sem juizo
        10.352719	11.851183	Onde canta o sabiá
        12.277413	16.010252	Meu vaqueiro meu peão
        """
        self.EXPECTED_CLIPS = [
            "1 - A saga de um vaqueiro.mp3",
            "2 - Brincar de amar.mp3",
            "3 - A praia.mp3",
            "4 - Menino sem juizo.mp3",
            "5 - Onde canta o sabiá.mp3",
            "6 - Meu vaqueiro meu peão.mp3"
        ]
    def test_ffmpegPath(self):
        assert self.ffmpegPath, "`%s` not found." % self.ffmpegPath

    def test_audio_extract_renaming_audio_files(self):
        extractor = AudioClipExtractor(self.audioPath, self.ffmpegPath)
        extractor.extractClips(self.LABELS_SAMPLE, constants.TESTS_DATA_DIR, titleInFile=True)

        for extractedClipPath, expectedClipPath in zip(
            [joinDataDir(self.EXPECTED_CLIPS[i]) for i in range(6)],
            [joinDataDir("expected_clip%d.mp3" % i) for i in range(1, 7)]):

            assert os.path.isfile(extractedClipPath), \
                "'%s' not found" % extractedClipPath

            f_extracted = open(extractedClipPath, 'rb')
            f_expected = open(expectedClipPath, 'rb')

            # Compare files
            try:
                assert f_extracted.read() == f_expected.read(), \
                    "'%s' It doesn't match expected data" % expectedClipPath
            except(AssertionError) as e:
                f_expected.close()
                f_extracted.close()

                os.unlink(extractedClipPath)

            if os.path.isfile(extractedClipPath):
                os.unlink(extractedClipPath)
    
    def test_audio_extract(self):
        extractor = AudioClipExtractor(self.audioPath, self.ffmpegPath)
        extractor.extractClips(self.specsPath, constants.TESTS_DATA_DIR)

        for extractedClipPath, expectedClipPath in zip(
            [joinDataDir("clip%d.mp3" % i) for i in range(1, 7)],
            [joinDataDir("expected_clip%d.mp3" % i) for i in range(1, 7)]):

            assert os.path.isfile(extractedClipPath), \
                "'%s' not found" % extractedClipPath

            f_extracted = open(extractedClipPath, 'rb')
            f_expected = open(expectedClipPath, 'rb')

            # Compare files
            try:
                assert f_extracted.read() == f_expected.read(), \
                    "'%s' It doesn't match expected data" % expectedClipPath
            except(AssertionError) as e:
                f_expected.close()
                f_extracted.close()

                os.unlink(extractedClipPath)

            if os.path.isfile(extractedClipPath):
                os.unlink(extractedClipPath)

    def test_audio_extract_with_zip_archiving(self):
        extractor = AudioClipExtractor(self.audioPath, self.ffmpegPath)
        extractor.extractClips(self.specsPath, constants.TESTS_DATA_DIR, zipOutput=True)

        extractedZipPath = joinDataDir('synthesized_speech_clips.zip')
        expectedZipPath = joinDataDir('expected_archive.zip')

        assert os.path.isfile(extractedZipPath), \
            "'%s' not found" % extractedZipPath

        f_extracted = open(extractedZipPath, 'rb')
        f_expected = open(expectedZipPath, 'rb')

        try:
            assert f_extracted.read() == f_expected.read(), \
                "'%s' It doesn't match expected data" % extractedZipPath
        except(AssertionError) as e:
            f_expected.close()
            f_extracted.close()

            os.unlink(extractedZipPath)
