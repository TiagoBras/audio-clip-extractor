# -*- coding: utf-8 -*-
import sys
import os
import pytest
from tests import constants

sys.path.insert(0, constants.ROOT_DIR)

from audioclipextractor.parser import SpecsParser, AudioClipSpec


def almostEqual(x, y):
    return abs(x - y) < 0.0001


class TestAudioClipSpec(object):
    def test_initializer(self):
        s = AudioClipSpec(10.5, 20, 'Hello World!')
        assert almostEqual(s.start, 10.5)
        assert almostEqual(s.end, 20)
        assert s.text == 'Hello World!'

        # Check if text is an empty string as default
        assert AudioClipSpec(0, 1).text == ''

    def test_initializer_when_start_is_greater_or_equal_than_end(self):
        with pytest.raises(ValueError):
            AudioClipSpec(2.0, 1.0)

        with pytest.raises(ValueError):
            AudioClipSpec(1.054, 1.054)

    def test_initializer_when_start_or_end_are_negative(self):
        with pytest.raises(ValueError):
            AudioClipSpec(-2.4, 5.0)

        with pytest.raises(ValueError):
            AudioClipSpec(0.5, -30.7)

        with pytest.raises(ValueError):
            AudioClipSpec(-3.5, -1.4)

    def test_properties_with_valid_values(self):
        s = AudioClipSpec(1.0, 5.0, 'James')
        assert almostEqual(s.start, 1.0)
        assert almostEqual(s.end, 5.0)
        assert s.text == 'James'

        s.start = 4.0
        assert almostEqual(s.start, 4.0)

        s.end = 7.954
        assert almostEqual(s.end, 7.954)

        s.text = 'Winter is coming'
        assert s.text == 'Winter is coming'

    def test_properties_with_invalid_values(self):
        s = AudioClipSpec(1.0, 5.0, 'James')

        # When <start> is negative
        with pytest.raises(ValueError):
            s.start = -5.0

        # When <start> is equal or greater than <end>
        with pytest.raises(ValueError):
            s.start = 6.0

        # When <end> is negative
        with pytest.raises(ValueError):
            s.end = -5.0

        # When <end> is equal or greater than <end>
        with pytest.raises(ValueError):
            s.end = 0.5

    def test_duration(self):
        s = AudioClipSpec(1.0, 5.5)
        assert almostEqual(s.duration(), 4.5)

        s = AudioClipSpec(12.436, 54.703)
        assert almostEqual(s.duration(), 42.267)


class TestSpecsParser:
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
            AudioClipSpec(0.303745, 0.861787, "Hello"),
            AudioClipSpec(1.570524, 2.618325, "My name is Harry,"),
            AudioClipSpec(2.818466, 4.292451, "and I'm a software engineer."),
            AudioClipSpec(4.731815, 9.730024,
                          "I've been working on a big project for the last 5 years which I'll soon reveal to the world."),
            AudioClipSpec(10.352719, 11.851183, "People will be amazed by it."),
            AudioClipSpec(12.277413, 16.010252, "I'd even dare to say that cats and dogs are going to love it as much.")
        ]

    def test_parse_line_with_valid_input(self):
        s = SpecsParser._parse_line('1.0 7.5 You shall not pass!')
        assert almostEqual(s.start, 1.0)
        assert almostEqual(s.end, 7.5)
        assert s.text == 'You shall not pass!'

        # With more whitespace and no text
        s = SpecsParser._parse_line('   1.0   7.5 Go!    ')
        assert almostEqual(s.start, 1.0)
        assert almostEqual(s.end, 7.5)
        assert s.text == 'Go!'

        # With more whitespace and no text
        s = SpecsParser._parse_line('   1.0   7.5')
        assert almostEqual(s.start, 1.0)
        assert almostEqual(s.end, 7.5)
        assert s.text == ''

    def test_parse_line_with_invalid_input(self):
        with pytest.raises(ValueError):
            SpecsParser._parse_line('    7.5    ValueError!  23.7 ')

        with pytest.raises(ValueError):
            SpecsParser._parse_line('  2.5 ')

    def test_read_labels_from_string(self):
        clips = SpecsParser.parse(self.LABELS_SAMPLE)

        assert clips is not None
        NUM_OF_CLIPS = 6
        assert len(clips) == NUM_OF_CLIPS

        for i in range(NUM_OF_CLIPS):
            assert abs(clips[i].duration() - self.EXPECTED_CLIPS[i].duration()) < 0.0001
            assert clips[i].text == self.EXPECTED_CLIPS[i].text

    def test_read_labels_from_file(self):
        specs_path = os.path.join(constants.TESTS_DATA_DIR, 'synthesized_speech.txt')
        clips = SpecsParser.parse(specs_path)

        assert clips is not None
        NUM_OF_CLIPS = 6
        assert len(clips) == NUM_OF_CLIPS

        for i in range(NUM_OF_CLIPS):
            assert abs(clips[i].duration() - self.EXPECTED_CLIPS[i].duration()) < 0.0001
            assert clips[i].text == self.EXPECTED_CLIPS[i].text

    def test_read_labels_from_string_with_no_text(self):
        NUM_OF_CLIPS = 5
        labels = """
        0.5 20 Foo
        34  50
        103.44 130
        150 173 Bar
        .203 205.
        """
        specs = SpecsParser.parse(labels)

        assert specs
        assert len(specs) == NUM_OF_CLIPS

        expected_specs = [
            AudioClipSpec(start=0.5, end=20, text="Foo"),
            AudioClipSpec(start=34, end=50, text=""),
            AudioClipSpec(start=103.44, end=130, text=""),
            AudioClipSpec(start=150, end=173, text="Bar")
        ]

        for spec, expectedSpec in zip(specs, expected_specs):
            assert abs(spec.duration() - expectedSpec.duration()) < 0.0001
            assert spec.text == expectedSpec.text
