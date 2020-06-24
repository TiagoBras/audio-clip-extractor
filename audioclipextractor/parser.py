# -*- coding: utf-8 -*-
import os
import re


class AudioClipSpec(object):
    """Clip specification.

    Arguments and Attributes:
        start (float): start timestamp
        end (float): end timestamp
        text (str): clip metadata

    Raises:
        ValueError: `start` and `end` can't be negative
        ValueError: `start` can't be equal or greater than `end`
    """

    def __init__(self, start, end, text='', track=1):
        super(AudioClipSpec, self).__init__()
        self._start = float(start)
        self._end = float(end)
        self._text = text
        self._track = track

        if self._start < 0.0 or self._end < 0.0:
            raise ValueError("<start> or <end> can't be less than 0")

        if self._start >= self._end:
            raise ValueError("<start> can't be equal or greater than <end>, %2f >= %2.f", self._start, self._end)

    def duration(self):
        """Returns the duration of the clip (`end` - `start`)"""
        return self.end - self.start

    def __repr__(self):
        return "<AudioClipSpec start:%.2f, end:%.2f, text:'%s'>" % (self._start, self._end, self._text)

    # Property: start
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if value < 0.0:
            raise ValueError("<value> can't be less than 0")

        if value >= self._end:
            raise ValueError("<start> can't be equal or greater than <end>, %2f >= %2.f", value, self._end)
        self._start = value

    # Property: end
    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        if value < 0.0:
            raise ValueError("<value> can't be less than 0")

        if value <= self._start:
            raise ValueError("<end> can't be less or equal than <start>, %2f <= %2.f", value, self._start)
        self._end = value

    # Property: text
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    # Property: track
    @property
    def track(self):
        return self._track

    @track.setter
    def track(self, value):
        self._track = value


class SpecsParser(object):
    """Audio clip specifications' parser"""
    _PROG = re.compile(r'''^\s*(?P<begin>\d*\.?\d+)\s+  # start timestamp
                           (?P<end>\d*\.?\d+)           # end timestamp
                           (?P<text>.*)$                # text metadata
                        ''', re.X)

    @classmethod
    def parse(cls, specs_file_or_string):
        """Parsers a file or string and returns a list of AudioClipSpec
        
        Arguments:
            specs_file_or_string (str): specifications' file or string
        
        Examples:
            >>> SpecsParser.parse('23.4 34.1\n40.2 79.65 Hello World!')
            [<AudioClipSpec start:23.40, end:34.10, text:''>, 
            <AudioClipSpec start:40.20, end:79.65, text:'Hello World!'>]

        Returns: list(AudioClipSpec) or None
        """
        string_to_parse = None

        # Read the contents of the file if specs_file_or_string is not a string
        if os.path.isfile(specs_file_or_string):
            with open(specs_file_or_string, 'r') as f:
                string_to_parse = f.read()
        else:
            string_to_parse = specs_file_or_string

        # Audacity uses \r for newlines
        lines = [x.strip() for x in re.split(r'[\r\n]+', string_to_parse)]

        clips = []
        track = 1
        for line in lines:
            if line != '':
                clips.append(cls._parse_line(line, track))
                track = track + 1

            # if spec != None:
            #     clips.append(spec)

        return clips

    @classmethod
    def _parse_line(cls, line, track=1):
        """Parsers a single line of text and returns an AudioClipSpec

        Line format:
            <number> <number> [<text>]

        Returns: list(AudioClipSpec) or None
        """
        r = cls._PROG.match(line)

        if not r:
            raise ValueError("Error: parsing '%s'. Correct: \"<number> <number> [<text>]\"" % line)

        d = r.groupdict()

        if len(d['begin']) == 0 or len(d['end']) == 0:
            raise ValueError("Error: parsing '%s'. Correct: \"<number> <number> [<text>]\"" % line)

        return AudioClipSpec(d['begin'], d['end'], d['text'].strip(), track)
