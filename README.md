Audio Clip Cutter
=================

This utility allows one to cut multiple clips from a single or multiple audio files.

The idea of this project came up when I was doing some [Shadowing](https://en.wikipedia.org/wiki/Speech_shadowing), Japanese to be specific. The problem was that the dialogs were long, so if I wanted to practice a certain phrase or word I would have to manually rewind it. So I thought, if I can split them in different files I'll be able to practice each separately.

Also, since this script can embed text as metadata in the outputted clips themselves the next step would be to create an application (I'm thinking mobile first) that takes all these clips and automatically arranges them in a way that makes shadowing even easier to practice.


Requirements
------------

*FFMPEG* executable is mandatory to be able to run this. It can be downloaded for free
 [here](https://ffmpeg.org/download.html).

 After installing it, you can either add it to your *PATH*
 or pass it as an argument `--ffmpeg <ffmpegPath>`.

For each audio file there needs to be a file with the same name but with **.txt** extension with the clips timestamps (check section **How it works** for further information).

Note: *In future versions it will be possible to pass timestamps as optional arguments.*


How to install
--------------

Use **pip** with following command:

 ```Bash
    $ pip install audioclipcutter
 ```


How it works
------------

```
$ audioclipcutter audio_to_cut_from.mp3 `

```

The script looks for a file with the same name as the audio file but with the extension **.txt**. The format of this file is the same as the track labels' file that you can export using [Audacity](http://www.audacityteam.org/) by going to the menu **File > Export Labels...** or **Tracks > Edit Labels...** and then **Export**.

```
<begin_clip:seconds> <end_clip:seconds> [<text>]
```

Example:

```
1.50    6.20    Hello World!
10      24.70   Because I said so.
33.85   36
```

The `<text>` part is completely optional, but if provided it will be embedded in the respective outputted clip as metadata. The default name is `m_text` but it can be set by passing the option argument `--text-var <desired_name>` or `-m <desired_name>`.

It can also be piped to, example:

```
$ find . -name '*.mp3' -type f | audioclipcutter --zip
```

But since we can't have a single specifications file for multiple audio files, this isn't very useful yet. In the future we will be able to, for instance, cut out the first 15s for each file.


Arguments
---------

```
--version, -V
    Displays the version of the script

--zip, -z
    Archives the output in a zip container

--ffmpeg <FILEPATH>
    Sets the FFMPEG executable path

--output-dir, -o
    Sets the output directory

--text-var, -m
    Sets the name of the embedded text variable

[files]
    Audio files to process
```

Notes
-----

<To write about using the code>
