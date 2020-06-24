Audio Clip Extractor
====================

This utility allows one to cut multiple clips from a single or multiple audio files.

The idea of this project came up when I was doing some [Shadowing](https://en.wikipedia.org/wiki/Speech_shadowing). The problem was that the dialogs were long, so if I wanted to practice a certain phrase or word I would have to manually rewind it. So I thought, if I can split them in different files I'd be able to practice each separately.

Also, since this script can embed text as metadata in the outputted clips themselves the next step would be to create an application that takes all these clips and automatically arranges them in a way that makes shadowing even easier to practice.


Requirements
------------

This project depends on *FFMPEG*. It can be downloaded for free
 [here](https://ffmpeg.org/download.html).
After installing it, you can either add it to your *PATH* or pass it as an argument `--ffmpeg <ffmpeg_path>`.

For each audio file there needs to be a file with the same name but with **.txt** extension with the respective clips' timestamps (check under section **How it works** for further information).

Note: *In future versions it will be possible to pass timestamps as optional arguments.*


Installation
------------

Use **pip** with following command:

 ```Bash
    $ pip install audioclipextractor
 ```


How it works
------------

```
$ ace audio_to_cut_from.mp3

```

The script looks for a file with the same name as the audio file but with the extension **.txt**. The format of this file is the same as the track labels' file that you can export using [Audacity](http://www.audacityteam.org/) by going to the menu **File > Export Labels...** or **Tracks > Edit Labels...** and then **Export**.

```
<begin_clip:seconds> <end_clip:seconds> [<text>]
```

*Begin clip* **CANNOT** be equal to or greater than *End clip*. 


**Example:**

```
1.50    6.20    Hello World!
10      24.70   Because I said so.
33.85   36
```

The `<text>` part is completely optional, but if provided it will be embedded in the respective outputted clip as metadata. The default name is `m_text` but it can be set by passing the option argument `--text-var <desired_name>` or `-m <desired_name>`.

It can also be piped to, example:

```
$ find . -name '*.mp3' -type f | audioclipextractor --zip
```

But since we can't have a single specifications file for multiple audio files, this isn't very useful yet. In the future we will be able to, for instance, cut out the first 15s for each file.


Comand Line Options
-------------------

```
--version, -V
    Prints the version of the script

--zip, -z
    Archive the output in a zip container

--ffmpeg <FILEPATH>
    Specify the FFMPEG executable path

--output-dir, -o
    Set the output directory

--text-name, -m
    Specify the name of the embedded text variable

[files]
    Audio files to process
```

How to use it in your projects
------------------------------

I recommend installing [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) 
to create an isolated environment.

**Example:**

```
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install audioclipextractor
(venv) $ ace audio_to_cut_from.mp3
```

example.py

```Python
from audioclipextractor import AudioClipExtractor, SpecsParser

# Inicialize the extractor
ext = AudioClipExtractor('/path/to/audio/file.mp3', '/path/to/ffmpeg')

# Define the clips to extract
# It's possible to pass a file instead of a string
specs = '''
    3.5     17      Winter is coming.
    26      32.4    Summer child.
    40      58.9    Hodor. Hodor. Hodor.
'''

# Extract the clips according to the specs and save them as a zip archive
ext.extract_clips(specs, '/path/to/output/directory', zip_output=True)
```


Notes
-----

This is still a work in progress. Feel free to use it, fork it and give suggestions.


License
-------

AudioClipCutter is available under the [MIT License](http://opensource.org/licenses/MIT).
