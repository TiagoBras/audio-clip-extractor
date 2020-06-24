# -*- coding: utf-8 -*-
import sys
import os
import shutil
from tests import constants
from audioclipextractor.core import AudioClipExtractor, slugify_filename

sys.path.insert(0, constants.ROOT_DIR)


def find_file_recursively(filename, directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f == filename:
                return os.path.join(root, f)

    return None


def join_data_dir(filename):
    return os.path.join(constants.TESTS_DATA_DIR, filename)


class TestAudioClipExtractor:
    def setup_class(self):
        filename = 'ffmpeg.exe' if sys.platform == "win32" else 'ffmpeg'

        # First: looks for the executable recursively in ROOT_DIR
        ffmpeg_path = find_file_recursively(filename, constants.ROOT_DIR)

        if not ffmpeg_path:
            # Second: looks for the executable in PATH
            ffmpeg_path = shutil.which(filename)

        self.ffmpeg_path = ffmpeg_path
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
            "1-a-saga-de-um-vaqueiro.mp3",
            "2-brincar-de-amar.mp3",
            "3-a-praia.mp3",
            "4-menino-sem-juizo.mp3",
            "5-onde-canta-o-sabia.mp3",
            "6-meu-vaqueiro-meu-peao.mp3"
        ]

    def test_ffmpeg_path(self):
        assert self.ffmpeg_path, "`%s` not found." % self.ffmpeg_path

    def test_audio_extract_renaming_audio_files(self):
        extractor = AudioClipExtractor(self.audioPath, self.ffmpeg_path)
        extractor.extract_clips(self.LABELS_SAMPLE, constants.TESTS_DATA_DIR, text_as_title=True)

        for extracted_clip_path, expected_clip_path in zip(
                [join_data_dir(self.EXPECTED_CLIPS[i]) for i in range(6)],
                [join_data_dir("expected_clip%d.mp3" % i) for i in range(1, 7)]):

            assert os.path.isfile(extracted_clip_path), \
                "'%s' not found" % extracted_clip_path

            f_extracted = open(extracted_clip_path, 'rb')
            f_expected = open(expected_clip_path, 'rb')

            # Compare files
            try:
                assert f_extracted.read() == f_expected.read(), \
                    "'%s' It doesn't match expected data" % expected_clip_path
            except AssertionError as e:
                f_expected.close()
                f_extracted.close()

                os.unlink(extracted_clip_path)

            if os.path.isfile(extracted_clip_path):
                os.unlink(extracted_clip_path)

    def test_audio_extract(self):
        extractor = AudioClipExtractor(self.audioPath, self.ffmpeg_path)
        extractor.extract_clips(self.specsPath, constants.TESTS_DATA_DIR)

        for extracted_clip_path, expected_clip_path in zip(
                [join_data_dir("clip%d.mp3" % i) for i in range(1, 7)],
                [join_data_dir("expected_clip%d.mp3" % i) for i in range(1, 7)]):

            assert os.path.isfile(extracted_clip_path), \
                "'%s' not found" % extracted_clip_path

            f_extracted = open(extracted_clip_path, 'rb')
            f_expected = open(expected_clip_path, 'rb')

            # Compare files
            try:
                assert f_extracted.read() == f_expected.read(), \
                    "'%s' It doesn't match expected data" % expected_clip_path
            except AssertionError as e:
                f_expected.close()
                f_extracted.close()

                os.unlink(extracted_clip_path)

            if os.path.isfile(extracted_clip_path):
                os.unlink(extracted_clip_path)

    def test_audio_extract_with_zip_archiving(self):
        extractor = AudioClipExtractor(self.audioPath, self.ffmpeg_path)
        extractor.extract_clips(self.specsPath, constants.TESTS_DATA_DIR, zip_output=True)

        extracted_zip_path = join_data_dir('synthesized_speech_clips.zip')
        expected_zip_path = join_data_dir('expected_archive.zip')

        assert os.path.isfile(extracted_zip_path), \
            "'%s' not found" % extracted_zip_path

        f_extracted = open(extracted_zip_path, 'rb')
        f_expected = open(expected_zip_path, 'rb')

        try:
            assert f_extracted.read() == f_expected.read(), \
                "'%s' It doesn't match expected data" % extracted_zip_path
        except AssertionError as e:
            f_expected.close()
            f_extracted.close()

            os.unlink(extracted_zip_path)

    def test_slugify(self):
        pairs = [
            ("hello world.txt", "hello-world.txt"),
            ("Don't speak.OK?.wav", "dont-speakok.wav"),
            ("Cool File", "cool-file")
        ]

        for p in pairs:
            assert slugify_filename(p[0]) == p[1]
