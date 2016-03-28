from sys import platform as PLATFORM
from os.path import isfile
from subprocess import Popen, PIPE

from audioextractor.labels_parser import UdacityLabelsParser

class LabelsFormat:
    DEFAULT = 0
    UDACITY = 1

class AudioExtractor(object):
    """docstring for AudioExtractor"""
    def __init__(self, audioFilePathOrData, ffmpegPath=None):
        super(AudioExtractor, self).__init__()
        self.audioFilePath = audioFilePathOrData if isfile(audioFilePathOrData) else None
        self.audioData = audioFilePathOrData if self.audioFilePath == None else None
        self.ffmpegPath = ffmpegPath if ffmpegPath != None else self._ffmpegPath()

    def extractClips(self, labelsFileOrString, labelsFormat=LabelsFormat.UDACITY):
        parser = None

        if labelsFormat == LabelsFormat.UDACITY:
            parser = UdacityLabelsParser(labelsFileOrString)

        clips = parser.parseClips()

        for i, clip in enumerate(clips):
            command = [self.ffmpegPath,
                '-f', 'm4a', '-i', 'pipe:0',
                '-ss', '%.3f' % clip.start,
                '-t', '%.3f' % clip.duration(),
                '-c', 'copy',
                '-map', '0',
                '-acodec', 'libmp3lame',
                '-ab', '128k',
                '-f', 'mp3', 'pipe:1'
            ]

            p = Popen(command, stdin=PIPE, stdout=PIPE, bufsize=10**8)

            # Send AUDIO DATA and get the CLIPPED DATA
            r_stdout, r_stderr = p.communicate(self._audioData())

            # 13 clips => clip01.mp3, clip12.mp3...
            filenameFormat = 'clip%%0%dd.mp3' % len(str(len(clips)))
            with open(filenameFormat % (i+1), 'wb') as f_out:
                f_out.write(r_stdout)

    def _ffmpegPath(self):
        if PLATFORM == 'win32':
            return 'ffmpeg.exe'
        else:
            return 'ffmpeg'

    def _audioData(self):
        if self.audioData == None and self.audioFilePath != None:
            with open(self.audioFilePath, 'rb') as f:
                self.audioData = f.read()

        return self.audioData
