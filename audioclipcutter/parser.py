# -*- coding: utf-8 -*-
from os.path import isfile
import re

class InputType:
    STRING = 0
    FILE = 1

class AudioClipSpec(object):
    """docstring for AudioClipSpec"""
    def __init__(self, start, end, text=''):
        super(AudioClipSpec, self).__init__()
        self.start = float(start)
        self.end = float(end)
        self.text = text

    def duration(self):
        return self.end - self.start

    def __repr__(self):
        return "(%f, %f, %s)" % (self.start, self.end, self.text)

class LabelsParser(object):
    """docstring for LabelsParser"""
    def __init__(self, fileOrString):
        super(LabelsParser, self).__init__()

        if isfile(fileOrString):
            self.inputType = InputType.FILE
        else:
            self.inputType = InputType.STRING

        self.inputValue = fileOrString

        begin = r'(?P<begin>\d+\.\d*|\d*\.\d+|\d+)'
        end = r'(?P<end>\d+\.\d*|\d*\.\d+|\d+)'
        text = r'(?P<text>.*)'

        regex = begin + r'\s+' + end + text

        self.linePattern = re.compile(regex)

    def parseClips(self):
        stringToParse = None

        if self.inputType == InputType.FILE:
            with open(self.inputValue, 'r') as f:
                stringToParse = f.read()
        else:
            stringToParse = self.inputValue

        # Audacity uses \r for newlines
        lines = [x.strip() for x in re.split(r'[\r\n]+', stringToParse)]

        clips = []
        for line in lines:
            spec = self._parseLine(line)

            if spec != None:
                clips.append(spec)

        return clips

    def _parseLine(self, line):
        r = self.linePattern.search(line)

        if r == None:
            return None

        d = r.groupdict()

        if len(d['begin']) == 0 or len(d['end']) == 0:
            return None
        else:
            return AudioClipSpec(d['begin'], d['end'], d['text'].strip())
