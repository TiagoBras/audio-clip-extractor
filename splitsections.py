from subprocess import call, check_output, Popen
from os import remove
from os.path import exists, join
from zipfile import ZipFile
import re


files = [
	"1-01"
]

LABELS_DIR = 'labels'
AUDIO_DIR = 'audio'
ZIP_OUTPUT = "out.zip"
TMP_OUTPUT = "tmp.mp3"

def main():
	if exists(ZIP_OUTPUT):
		remove(ZIP_OUTPUT)

	with ZipFile(ZIP_OUTPUT, "w") as myzip:
		for f in files:
			for clip_spec in readClipSpecs(join(LABELS_DIR, f + '.txt')):
				if exists(TMP_OUTPUT):
					remove(TMP_OUTPUT)

				cmd_str = "ffmpeg -i %s -ss %.3f -t %.3f -c copy -map 0 -acodec libmp3lame -ab 128k %s"
				args = cmd_str % (join(AUDIO_DIR, f + '.m4a'), clip_spec.start, clip_spec.duration(), TMP_OUTPUT)

				print(args)
				call(args.split())

				myzip.write(TMP_OUTPUT, arcname=clip_spec.genFilename() + '.mp3')

	if exists(TMP_OUTPUT):
		remove(TMP_OUTPUT)

class Gender(object):
	Male = 0
	Female = 1

	@staticmethod
	def fromString(s):
		if s.lower() == 'f' or s.lower() == 'female':
			return Gender.Female
		else:
			return Gender.Male

	@staticmethod
	def toString(value, verbose=False):
		if value == Gender.Female:
			return 'female' if verbose else 'f'
		else:
			return 'male' if verbose else 'm'


class LanguageLevel(object):
	Normal = 0
	Casual = 1
	Formal = 2

	@staticmethod
	def fromString(s):
		if s.lower() == 'c' or s.lower() == 'casual':
			return LanguageLevel.Casual
		elif s.lower() == 'd' or s.lower() == 'formal':
			return LanguageLevel.Formal
		else:
			return LanguageLevel.Normal

	@staticmethod
	def toString(value, verbose=False):
		if value == LanguageLevel.Casual:
			return 'casual' if verbose else 'c'
		elif value == LanguageLevel.Formal:
			return 'formal' if verbose else 'd'
		else:
			return 'normal' if verbose else 'n'

class ClipSpec(object):
	def __init__(self, start, end, number=0, letter='a', gender='m', lang_level=''):
		super(ClipSpec, self).__init__()
		self.start = float(start)
		self.end = float(end)
		self.number = int(number)
		self.letter = letter
		self.gender = Gender.fromString(gender)
		self.lang_level = LanguageLevel.fromString(lang_level)

	def duration(self):
		return self.end - self.start

	def genFilename(self, prefix=''):
		if len(prefix) > 0:
			prefix.append('-')

		return "%s%02d-%c-%c-%c" % (
				prefix,
				self.number, 
				self.letter.upper(), 
				Gender.toString(self.gender).upper(),
				LanguageLevel.toString(self.lang_level).upper(),
			)

	def __repr__(self):
		return self.__unicode__()

	def __unicode__(self):
		return "%02d %c %c %c: %.3f" % (
			self.number, 
			self.letter.upper(), 
			Gender.toString(self.gender).upper(),
			LanguageLevel.toString(self.lang_level).upper(),
			self.duration()
		)

def readClipSpecs(filename):
	pattern = re.compile(r"""
		(?P<start>\d+[.]?\d*)\s+\d+[.]?\d*\s+
		(?P<number>\d*)
		(?P<letter>[ab])\s*
		(?P<gender>[fm]?)\s*
		(?P<level>[cd]?)
	""", re.VERBOSE)

	clip_specs = []
	with open(filename, 'r') as myfile:
		lines = re.split(r'[\r\n]+', myfile.read())
		for line1, line2 in zip(*[iter(lines)]*2):
			g1 = pattern.match(line1).groupdict()
			g2 = pattern.match(line2).groupdict()

			clip_spec = ClipSpec(g1['start'], g2['start'], g1['number'], g1['letter'], g1['gender'], g1['level'])
			clip_specs.append(clip_spec)

	return clip_specs
		
if __name__ == '__main__':
	main()





