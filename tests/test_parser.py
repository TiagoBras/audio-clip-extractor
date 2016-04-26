# -*- coding: utf-8 -*-
import sys
import os

import constants

sys.path.insert(0, constants.ROOT_DIR)

from audioclipcutter.parser import LabelsParser, AudioClipSpec

class TestLabelsParser:
    def setup_class(self):
        self.LABELS_SAMPLE = """
        0.303745	0.861787	Hello
        1.570524	2.618325	My name is Harry,
        2.818466	4.292451	and I'm a software engineer.
        4.731815	9.730024	I've been working on a big project for the last 5 years which I'll soon reveal to the world.
        10.352719	11.851183	People will be amazed by it.
        12.277413	16.010252	I'd even dare to say that cats and dogs are going to love it as much.
        """

        self.EXPECTED_CLIPS = [
            AudioClipSpec(start=0.303745, end=0.861787, text="Hello"),
            AudioClipSpec(start=1.570524, end=2.618325, text="My name is Harry,"),
            AudioClipSpec(start=2.818466, end=4.292451, text="and I'm a software engineer."),
            AudioClipSpec(start=4.731815, end=9.730024, text="I've been working on a big project for the last 5 years which I'll soon reveal to the world."),
            AudioClipSpec(start=10.352719, end=11.851183, text="People will be amazed by it."),
            AudioClipSpec(start=12.277413, end=16.010252, text="I'd even dare to say that cats and dogs are going to love it as much.")
        ]

    def test_read_labels_from_string(self):
        parser = LabelsParser(self.LABELS_SAMPLE)
        clips = parser.parseClips()

        assert clips != None
        NUM_OF_CLIPS = 6
        assert len(clips) == NUM_OF_CLIPS

        for i in range(NUM_OF_CLIPS):
            assert abs(clips[i].duration() - self.EXPECTED_CLIPS[i].duration()) < 0.0001
            assert clips[i].text == self.EXPECTED_CLIPS[i].text

    def test_read_labels_from_file(self):
        specsPath = os.path.join(constants.TESTS_DATA_DIR, 'synthesized_speech.txt')
        parser = LabelsParser(specsPath)
        clips = parser.parseClips()

        assert clips != None
        NUM_OF_CLIPS = 6
        assert len(clips) == NUM_OF_CLIPS

        for i in range(NUM_OF_CLIPS):
            assert abs(clips[i].duration() - self.EXPECTED_CLIPS[i].duration()) < 0.0001
            assert clips[i].text == self.EXPECTED_CLIPS[i].text
