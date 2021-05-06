# -*- coding: utf-8 -*-
import os
import zipfile
import subprocess
import re
import unicodedata
from pkg_resources import resource_filename, Requirement

from .parser import SpecsParser, AudioClipSpec


class AudioClipExtractor(object):
    """Extracts clips from audio files.
    
    Arguments:
        audio_file_path (str): Path to the file to extract clips from
        ffmpeg_path (str): Path to the ffmpeg executable

    Attributes:
        text_metadata_name (str) - getter/setter
            The variable name used to embed text in the output clip
    """

    def __init__(self, audio_file_path, ffmpeg_path="ffmpeg", bitrate="128k"):
        super(AudioClipExtractor, self).__init__()
        self._audioFilePath = audio_file_path
        self._ffmpeg_path = ffmpeg_path
        self._bitrate = bitrate
        self._textMetadataName = 'title'
        self._textMetadataTrack = 'track'

    @property
    def text_metadata_name(self):
        return self._textMetadataName

    @text_metadata_name.setter
    def text_metadata_name(self, value):
        self._textMetadataName = value

    def extract_clips(self, specs_file_path_or_str, output_dir=None, zip_output=False, text_as_title=False):
        """Extract clips according to the specification file or string.
        
        Arguments:
            specs_file_path_or_str (str): Specification file path or string
            output_dir (str): Location of the extracted clips
            zip_output (bool): Archive extracted clips' flag
            text_as_title (str): Include clip text in filename

        Specifications format:
            <begin:seconds> <end:seconds> [<text_metadata>]

            20.5    59.75   Discussion about dogs
            105.3   200.3   Cat story

        Notes:
            <text_metadata> is completely optional
        """
        clips = SpecsParser.parse(specs_file_path_or_str)

        # Output to current working directory if no output_dir was provided
        if not output_dir:
            output_dir = os.path.abspath('.')

        zip_file = None
        if zip_output:
            bname = os.path.splitext(os.path.basename(specs_file_path_or_str))[0]
            zip_path = "%s_clips.zip" % bname
            zip_file = zipfile.ZipFile(os.path.join(output_dir, zip_path), mode='w')

        for i, clip in enumerate(clips):
            # 13 clips => clip01.wav, clip12.wav...
            if text_as_title:
                filename_format = '%%0%dd - ' % len(
                    str(len(clips))) + '%s.wav' % clip.text if clip.text != '' else 'clip'
            else:
                filename_format = 'clip%%0%dd.wav' % len(str(len(clips)))

            filepath = os.path.join(output_dir, slugify_filename(filename_format % (i + 1)))

            clip_data = self._extract_clip_data(clip)

            with open(filepath, 'wb') as f_out:
                f_out.write(clip_data)

            if zip_file:
                zip_file.write(filepath, arcname=os.path.basename(filepath))
                os.unlink(filepath)

        if zip_file:
            zip_file.close()

    def _extract_clip_data(self, audio_clip_spec, show_logs=False):
        """Extracts a single clip according to audioClipSpec.

        Arguments:
            audio_clip_spec (AudioClipSpec): Clip specification
            show_logs (bool): Show ffmpeg output
        """
        command = [self._ffmpeg_path]

        if not show_logs:
            command += ['-nostats', '-loglevel', '0']

        command += [
            '-i', self._audioFilePath,
            '-ss', '%.3f' % audio_clip_spec.start,
            '-t', '%.3f' % audio_clip_spec.duration(),
            '-c', 'copy',
            '-map', '0',
            '-acodec', 'pcm_s16le',
            '-ab', self._bitrate,
            '-f', 'wav'
        ]

        # Add clip TEXT as metadata and set a few more to default
        metadata = {self._textMetadataName: audio_clip_spec.text,
                    self._textMetadataTrack: audio_clip_spec.track}

        for k, v in metadata.items():
            command.append('-metadata')
            command.append("{}='{}'".format(k, v))

        command.append('pipe:1')

        return subprocess.check_output(command)


def slugify_filename(filename):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """

    def slugify(value):
        value = unicode(value)
        value = unicode(unicodedata.normalize('NFKD', value).encode('ascii', 'ignore'))
        value = unicode(re.sub(r"[^\w\s-]", '', value).strip().lower())

        return unicode(re.sub(r"[-\s]+", '-', value))

    ext_dot_index = filename.rfind('.')

    if 0 < ext_dot_index < len(filename) - 1:
        ext = slugify(filename[ext_dot_index:])
        filename = filename[:ext_dot_index+1]

        return slugify(filename) + unicode(".") + ext
    else:
        return slugify(filename)


def unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        return unicode_or_str
    else:
        return unicode_or_str.decode("ascii")
