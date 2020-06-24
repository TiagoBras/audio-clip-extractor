# -*- coding: utf-8 -*-
import sys
import os
import pytest
import re
from tests import constants
import audioclipextractor.scripts.main as main

sys.path.insert(0, constants.ROOT_DIR)

FFMPEG = 'ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg'


def test_version_argument():
    assert re.search(r'\d+\.\d+\.\d+\w*', main.version())


def test_version_argument_when_there_is_no_version_defined():
    with pytest.raises(IOError):
        # There no VERSION file in tests folder
        main.version(constants.TESTS_DIR)


def test_passing_skip_path_lookup():
    # It should exit with code 1 since there's no ffmpeg
    with pytest.raises(SystemExit):
        main.run(['--skip-path-lookup'])
        assert pytest.capsys.readouterr()[0] == 1


def test_passing_ffmpeg_path_with_no_files():
    with pytest.raises(SystemExit):
        main.run(['--ffmpeg', os.path.join(constants.TESTS_DATA_DIR, FFMPEG)])
        assert pytest.capsys.readouterr()[0] == 2


def test_passing_ffmpeg_path_with_audio_filepath():
    args = [
        '--ffmpeg', os.path.join(constants.TESTS_DATA_DIR, FFMPEG),
        '--output-dir', constants.TESTS_DATA_DIR,
        os.path.join(constants.TESTS_DATA_DIR, 'synthesized_speech.mp3')
    ]
    main.run(args)

    for i in range(1, 7):
        path = os.path.join(constants.TESTS_DATA_DIR, "clip%d.mp3" % i)

        assert os.path.isfile(path), "'%s' not found" % path

        os.unlink(path)


def test_zip_option():
    args = [
        '--ffmpeg', os.path.join(constants.TESTS_DATA_DIR, FFMPEG),
        '--output-dir', constants.TESTS_DATA_DIR,
        '--zip',
        os.path.join(constants.TESTS_DATA_DIR, 'synthesized_speech.mp3')
    ]
    main.run(args)

    path = os.path.join(constants.TESTS_DATA_DIR, 'synthesized_speech_clips.zip')

    assert os.path.isfile(path), "'%s' not found" % path

    os.unlink(path)


def test_passing_an_audio_file_with_no_matching_spec():
    args = [
        '--ffmpeg', os.path.join(constants.TESTS_DATA_DIR, FFMPEG),
        '--output-dir', constants.TESTS_DATA_DIR,
        os.path.join(constants.TESTS_DATA_DIR, 'expected_clip1.mp3')
    ]

    with pytest.raises(SystemExit):
        main.run(args)
        assert pytest.capsys.readouterr()[0] == 3


def test_passing_spec():
    args = [
        '--ffmpeg', os.path.join(constants.TESTS_DATA_DIR, FFMPEG),
        '--output-dir', constants.TESTS_DATA_DIR,
        '--text-as-title',
        os.path.join(constants.TESTS_DATA_DIR, 'synthesized_speech.mp3')
    ]

    main.run(args)

    file_paths = map(lambda x: os.path.join(constants.TESTS_DATA_DIR, x), [
        "1-hello.mp3",
        "2-my-name-is-harry.mp3",
        "3-and-im-a-software-engineer.mp3",
        "4-ive-been-working-on-a-big-project-for-the-last-5-years-which-ill-soon-reveal-to-the-world.mp3",
        "5-people-will-be-amazed-by-it.mp3",
        "6-id-even-dare-to-say-that-cats-and-dogs-are-going-to-love-it-as-much.mp3"
    ])

    for path in file_paths:
        assert os.path.isfile(path)

        os.unlink(path)
