from audioextractor.labels_parser import UdacityLabelsParser, AudioClip

class TestUdacityLabelsParser:
    def setup(self):
        self.LABELS_SAMPLE = """
        5.749493	5.749493	1a f c
        6.328176	6.328176	1a
        7.012639	7.012639	1b m c
        7.367316	7.367316	1b"""

        self.EXPECTED_CLIPS = [
            AudioClip(start=5.749493, end=6.328176, metadata='1a f c'),
            AudioClip(start=7.012639, end=7.367316, metadata='1b m c')
        ]

    def test_read_labels_from_string(self):
        parser = UdacityLabelsParser(self.LABELS_SAMPLE)
        clips = parser.parseClips()

        assert clips != None
        assert len(clips) == 2
        assert abs(clips[0].duration() - self.EXPECTED_CLIPS[0].duration()) < 0.0001
        assert abs(clips[1].duration() - self.EXPECTED_CLIPS[1].duration()) < 0.0001
        assert clips[0].metadata == self.EXPECTED_CLIPS[0].metadata
        assert clips[1].metadata == self.EXPECTED_CLIPS[1].metadata

    def test_read_labels_from_file(self):
        parser = UdacityLabelsParser('tests/data/labels_data.txt')
        clips = parser.parseClips()

        assert clips != None
        assert len(clips) == 2
        assert abs(clips[0].duration() - self.EXPECTED_CLIPS[0].duration()) < 0.0001
        assert abs(clips[1].duration() - self.EXPECTED_CLIPS[1].duration()) < 0.0001
        assert clips[0].metadata == self.EXPECTED_CLIPS[0].metadata
        assert clips[1].metadata == self.EXPECTED_CLIPS[1].metadata

    # def test_read_labels_from_string_as_class_method():
    #     clips = UdacityLabelsParser.parseClips(LABELS_SAMPLE)
    #
    #     clip1 = AudioClip(start=5.749493, end=6.328176)
    #     clip2 = AudioClip(start=7.012639, end=7.367316)
    #
    #     assert clip1.duration() == 0.578682
    #     assert clip1.metadata == "1a f c"
    #     assert clip2.duration() == 0.354676
    #     assert clip2.metadata == "1b m c"
