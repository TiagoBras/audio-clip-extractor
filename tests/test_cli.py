# -*- coding: utf-8 -*-
import sys
import os
import pytest

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT_DIR)

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_DATA_DIR = os.path.join(TESTS_DIR, 'data')

import audioclipcutter.scripts.main as main

FFMPEG = 'ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg'

def setup_module(module):
    pass

def test_passing_skip_path_lookup():
    # It should exit with code 1 since there's no ffmpeg
    with pytest.raises(SystemExit) as cm:
        main.run(['--skip-path-lookup'])
        assert pytest.capsys.readouterr()[0] == 1

def test_passing_ffmpeg_path_with_no_files():
    with pytest.raises(SystemExit) as cm:
        main.run(['--ffmpeg', os.path.join(TESTS_DATA_DIR, FFMPEG)])
        assert pytest.capsys.readouterr()[0] == 2

def test_passing_ffmpeg_path_with_audio_filepath():
    args = [
        '--ffmpeg', os.path.join(TESTS_DATA_DIR, FFMPEG),
        '--output-dir', TESTS_DATA_DIR,
        os.path.join(TESTS_DATA_DIR, 'synthesized_speech.mp3')
    ]
    main.run(args)

    for i in range(1, 7):
        path = os.path.join(TESTS_DATA_DIR, "clip%d.mp3" % i)

        assert os.path.isfile(path), "'%s' not found" % path

        os.unlink(path)

def test_zip_option():
    args = [
        '--ffmpeg', os.path.join(TESTS_DATA_DIR, FFMPEG),
        '--output-dir', TESTS_DATA_DIR,
        '--zip',
        os.path.join(TESTS_DATA_DIR, 'synthesized_speech.mp3')
    ]
    main.run(args)

    path = os.path.join(TESTS_DATA_DIR, 'synthesized_speech_clips.zip')

    assert os.path.isfile(path), "'%s' not found" % path

    os.unlink(path)

def test_passing_an_audio_file_with_no_matching_spec():
    args = [
        '--ffmpeg', os.path.join(TESTS_DATA_DIR, FFMPEG),
        '--output-dir', TESTS_DATA_DIR,
        os.path.join(TESTS_DATA_DIR, 'expected_clip1.mp3')
    ]

    with pytest.raises(SystemExit) as cm:
        main.run(args)
        assert pytest.capsys.readouterr()[0] == 3
