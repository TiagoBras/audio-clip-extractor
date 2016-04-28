# -*- coding: utf-8 -*-
import os
import zipfile
import subprocess

from pkg_resources import resource_filename, Requirement

from .parser import SpecsParser, AudioClipSpec

class AudioClipExtractor(object):
    """Extracts clips from audio files.
    
    Arguments:
        audioFilePath (str): Path to the file to extract clips from
        ffmpegPath (str): Path to the ffmpeg executable

    Attributes:
        textMetadataName (str) - getter/setter
            The variable name used to embed text in the output clip
    """
    def __init__(self, audioFilePath, ffmpegPath):
        super(AudioClipExtractor, self).__init__()
        self._audioFilePath = audioFilePath
        self._ffmpegPath = ffmpegPath
        self._textMetadataName = 'm_text'

    @property
    def textMetadataName(self):
        return self._textMetadataName

    @textMetadataName.setter
    def textMetadataName(self, value):
        self._textMetadataName = value

    def extractClips(self, specsFilePathOrStr, outputDir=None, zipOutput=False):
        """Extract clips according to the specification file or string.
        
        Arguments:
            specsFilePathOrStr (str): Specification file path or string
            outputDir (str): Location of the extracted clips
            zipOutput (bool): Archive extracted clips' flag

        Specifications format:
            <begin:seconds> <end:seconds> [<text_metadata>]

            20.5    59.75   Discussion about dogs
            105.3   200.3   Cat story

        Notes:
            <text_metadata> is completely optional
        """
        clips = SpecsParser.parse(specsFilePathOrStr)

        # Output to current working directory if no outputDir was provided
        if not outputDir:
            outputDir = os.path.abspath('.')

        zipFile = None
        if zipOutput:
            bname = os.path.splitext(os.path.basename(specsFilePathOrStr))[0]
            zipPath = "%s_clips.zip" % bname
            zipFile = zipfile.ZipFile(os.path.join(outputDir, zipPath), mode='w')

        for i, clip in enumerate(clips):
            # 13 clips => clip01.mp3, clip12.mp3...
            filenameFormat = 'clip%%0%dd.mp3' % len(str(len(clips)))

            filepath = os.path.join(outputDir, filenameFormat % (i+1))

            clipData = self._extractClipData(clip)

            with open(filepath, 'wb') as f_out:
                f_out.write(clipData)

            if zipFile:
                zipFile.write(filepath, arcname=os.path.basename(filepath))
                os.unlink(filepath)

        if zipFile:
            zipFile.close()

    def _extractClipData(self, audioClipSpec, showLogs=False):
        """Extracts a single clip according to audioClipSpec.

        Arguments:
            audioClipSpec (AudioClipSpec): Clip specification
            showLogs (bool): Show ffmpeg output
        """
        command = [self._ffmpegPath]

        if not showLogs:
            command += ['-nostats', '-loglevel', '0']

        command += [
            '-i', self._audioFilePath,
            '-ss', '%.3f' % audioClipSpec.start,
            '-t', '%.3f' % audioClipSpec.duration(),
            '-c', 'copy',
            '-map', '0',
            '-acodec', 'libmp3lame',
            '-ab', '128k',
            '-f', 'mp3'
        ]

        # Add clip TEXT as metadata and set a few more to default
        metadata = { self._textMetadataName: audioClipSpec.text }

        for k, v in metadata.items():
            command.append('-metadata')
            command.append("{}='{}'".format(k, v))

        command.append('pipe:1')

        return subprocess.check_output(command)
