from os.path import isfile
import re

class InputType:
    STRING = 0
    FILE = 1

class AudioClip(object):
    """docstring for AudioClip"""
    def __init__(self, start, end, metadata=''):
        super(AudioClip, self).__init__()
        self.start = float(start)
        self.end = float(end)
        self.metadata = metadata

    def duration(self):
        return self.end - self.start

    def __repr__(self):
        return "(%f, %f, %s)" % (self.start, self.end, self.metadata)

class UdacityLabelsParser(object):
    """docstring for UdacityLabelsParser"""
    def __init__(self, fileOrString):
        super(UdacityLabelsParser, self).__init__()

        if isfile(fileOrString):
            self.inputType = InputType.FILE
        else:
            self.inputType = InputType.STRING

        self.inputValue = fileOrString

        self.linePattern = re.compile(r"""
    		(?P<timestamp>\d+[.]?\d*)\s+\d+[.]?\d*\s+
    		(?P<metadata>.*)""", re.VERBOSE)

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
        lineBuffer = []
        for line in lines:
            r = self._parseLine(line)

            if r != None:
                lineBuffer.append(r)

                # Create a Clip every 2 valid timestamps
                if len(lineBuffer) == 2:
                    clips.append(AudioClip(lineBuffer[0][0], lineBuffer[1][0], lineBuffer[0][1]))
                    lineBuffer[:] = []

        return clips


    def _parseLine(self, line):
        r = self.linePattern.match(line)

        if r == None:
            return None

        d = r.groupdict()

        if len(d['timestamp']) == 0:
            return None
        else:
            return [d['timestamp'], d['metadata']]
