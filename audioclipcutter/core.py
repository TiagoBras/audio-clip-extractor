# -*- coding: utf-8 -*-
from sys import platform as PLATFORM
from sys import exit
from os.path import isfile, isdir, join, abspath
from subprocess import Popen, PIPE

from pkg_resources import resource_filename, Requirement

from .audacity_parser import UdacityLabelsParser, AudioClipSpec

# import tbutils  # My utils library

class AudioClipCutter(object):
    def __init__(self, audioFilePathOrData, ffmpegPath=None):
        self.audioFilePathOrData = audioFilePathOrData
        self.ffmpegPath = ffmpegPath if ffmpegPath != None else self._ffmpegPath()
        self._audioFileData = None

    def extractClips(self, specsFilePathOrData, outputDir=''):
        parser = UdacityLabelsParser(specsFilePathOrData)

        clips = parser.parseClips()

        for i, clip in enumerate(clips):
            # 13 clips => clip01.mp3, clip12.mp3...
            filenameFormat = 'clip%%0%dd.mp3' % len(str(len(clips)))
            filepath = filenameFormat % (i+1)

            # Prepend directory to filepath if supplied
            if outputDir and isdir(outputDir):
                filepath = join(outputDir, filepath)

            clipData = self._extractClipData(clip)

            with open(filepath, 'wb') as f_out:
                f_out.write(clipData)

    def _extractClipData(self, audioClipSpec, showLogs=False):
        command = [self.ffmpegPath]

        if not showLogs:
            command += ['-nostats', '-loglevel', '0']

        command += [
            '-i', 'pipe:0',
            '-ss', '%.3f' % audioClipSpec.start,
            '-t', '%.3f' % audioClipSpec.duration(),
            '-c', 'copy',
            '-map', '0',
            '-acodec', 'libmp3lame',
            '-ab', '128k',
            '-f', 'mp3'
        ]

        # Add clip TEXT as metadata and set a few more to default
        metadata = dict(m_text=audioClipSpec.text)
            # title='Extracted clip',
            # album='N/A',
            # genre='Shadowing',
            # artist='N/A')

        for k, v in metadata.items():
            command.append('-metadata')
            command.append("{}='{}'".format(k, v))

        command.append('pipe:1')

        # stderr=open(devnull, 'w')
        p = Popen(command, stdin=PIPE, stdout=PIPE, bufsize=10**8)

        # Send AUDIO DATA and get the CLIPPED DATA
        r_stdout, r_stderr = p.communicate(self._audioData())

        return r_stdout

    def _ffmpegPath(self):
        ffmpegDir = resource_filename(Requirement.parse("audioclipcutter"), "audioclipcutter/bin")
        # ffmpegDir = resource_filename(__name__, 'bin')

        if PLATFORM == 'win32':
            return join(ffmpegDir, 'ffmpeg.exe')
        else:
            return join(ffmpegDir, 'ffmpeg')

    def _audioData(self):
        if self._audioFileData == None:
            self._audioFileData = self._readFileData(self.audioFilePathOrData)

        return self._audioFileData

    def _readFileData(self, filePathOrData):
        data = None
        try:
            none = self.filePathOrData.read()
        except Exception as e:
            pass

        if not data:
            try:
                with open(filePathOrData, 'rb') as f:
                    data = f.read()
            except Exception as e:
                raise

        return data

# class AudioExtractor(object):
#     """docstring for AudioExtractor"""
#     def __init__(self, audioFilePathOrData, ffmpegPath=None):
#         super(AudioExtractor, self).__init__()
#         self.audioFilePath = audioFilePathOrData if isfile(audioFilePathOrData) else None
#         self.audioData = audioFilePathOrData if self.audioFilePath == None else None
#         self.ffmpegPath = ffmpegPath if ffmpegPath != None else self._ffmpegPath()
#
#     def extractClips(self, labelsFileOrString, outputDir=None):
#         parser = UdacityLabelsParser(labelsFileOrString)
#
#         clips = parser.parseClips()
#
#         for i, clip in enumerate(clips):
#             # 13 clips => clip01.mp3, clip12.mp3...
#             filenameFormat = 'clip%%0%dd.mp3' % len(str(len(clips)))
#             filepath = filenameFormat % (i+1)
#
#             # Prepend directory to filepath if supplied
#             if outputDir and isdir(outputDir):
#                 filepath = join(outputDir, filepath)
#
#             clipData = self._extractClipData(clip)
#
#             with open(filepath, 'wb') as f_out:
#                 f_out.write(clipData)
#
#     def _extractClipData(self, audioClipSpec, showLogs=False):
#         command = [self.ffmpegPath]
#
#         if not showLogs:
#             command += ['-nostats', '-loglevel', '0']
#
#         command += [
#             '-i', 'pipe:0',
#             '-ss', '%.3f' % audioClipSpec.start,
#             '-t', '%.3f' % audioClipSpec.duration(),
#             '-c', 'copy',
#             '-map', '0',
#             '-acodec', 'libmp3lame',
#             '-ab', '128k',
#             '-f', 'mp3'
#         ]
#
#         # Add clip TEXT as metadata and set a few more to default
#         metadata = dict(m_text=audioClipSpec.text)
#             # title='Extracted clip',
#             # album='N/A',
#             # genre='Shadowing',
#             # artist='N/A')
#
#         for k, v in metadata.items():
#             command.append('-metadata')
#             command.append("{}='{}'".format(k, v))
#
#         command.append('pipe:1')
#
#         # stderr=open(devnull, 'w')
#         p = Popen(command, stdin=PIPE, stdout=PIPE, bufsize=10**8)
#
#         # Send AUDIO DATA and get the CLIPPED DATA
#         r_stdout, r_stderr = p.communicate(self._audioData())
#
#         return r_stdout
#
#     def _ffmpegPath(self):
#         ffmpegDir = resource_filename(Requirement.parse("AudioClipExtractor"), "audioextractor/bin")
#         # ffmpegDir = resource_filename(__name__, 'bin')
#
#         if PLATFORM == 'win32':
#             return join(ffmpegDir, 'ffmpeg.exe')
#         else:
#             return join(ffmpegDir, 'ffmpeg')
#
#     def _audioData(self):
#         if self.audioData == None and self.audioFilePath != None:
#             with open(self.audioFilePath, 'rb') as f:
#                 self.audioData = f.read()
#
#         return self.audioData
