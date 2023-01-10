# Python Script for m3u-Playlist-Creation in Linux, macOS and Windows

## Background

Recently I needed to write a script to create some m3u-playlists for SD-card for my car's audio system.
I have forked and improved [this repo](https://github.com/Zylence/m3u-Playlist-Creation-Script).

## Features
This script can be used to create music/video playlists on **Linux**, **macOS** and **Windows** with ease. It parses all subdirectories of a given directory (unless exclusions are set) and filters only for file types specified by the user. It offers additional options to remove duplicates and choose between absolute and relative paths.


## Usage

### Commandline Options:


|Option|Default|Description|
|------|-------|-----------|
|`-n`|`'playlist.m3u'`|The name of the playlist file, change it to your liking, but you need to keep the extension as is (.m3u).|
|`-m`|`'w'`|The mode python writes the playlist file in, the default, 'w' will overwrite existing files, use 'a' to append them instead.|
|`-c`|`'utf-8'`|Codec used by python when writing a file. Refer to the [Standard Encodings](https://docs.python.org/3/library/codecs.html#standard-encodings) section of the official docs for reference if you run into problems.
|`-s`|`os.getcwd()`|This searches the current working directory . I recommend setting an absolute path to your music directory or subfolder instead.|
|`-e`|`''`|Specifies the subdirectories that are not included in the playlist. (refer to the [Examples](https://github.com/Zylence/m3u-Playlist-Creation-Script/blob/main/README.md#examples) for usage information)|
|`-d`||If present this script will prevent duplicate entries in your playlist by only adding the first path found. (useful if the same tracks reside in multiple subfolders for some reason)|
|`-i`||If present this will add `#EXTINFO` tags into your playlist.|
|`-r`||If present this will result in your playlist containing paths relative to your current working directory.|
|`-f`|`'.mp3 .flac .wav .aac'`|Those are the formats the script will write into the playlist.

### Examples

#### Linux and MacOS
----------------

```console
python3 m3u.py
```
This runs the script with the default options, to be successful this requires the start of the script from inside your music library.


```console
python3 m3u.py -n 'my-playlist.m3u' -s '/path/to/my/music' -d
```
And that will result in a playlist called 'my-playlist.m3u' containing all the default music file formats from 'path/to/my/music' and all subdirectories without duplicates.



```console
python3 m3u.py -n 'my-playlist.m3u' -m 'a' -s '/path/to/my/music' -d -f '.mp3 .flac'
```
This command is similar to the one before, except it will not overwrite the existing file and only appends it by mp3 and flac files.


```console
python3 m3u.py -s '/path/to/my/music/Rock' -e 'Celtic Classic Gothic'
```
Lastly, that command will include all Rock  songs except those from the subdirectories: Celtic, Classic and Gothic.


#### Windows
---------------

The only thing that should differ is the way python is called (for my system that's `py` or `python`, the rest should be similar.

A command could look like this:

```console
py m3u.py -n 'my-playlist.m3u' -s 'C:/path/to/my/music/Rock' -d -f '.mp3 .flac'
```

### Note

* The playlist file is always created in the current working directory (that's where the script is run from).
* `-r` if set to True can result in unwanted behaviour if files from different folders have the same names but are not actually the same song. I recommend leaving this off, unless you know you got a lot of actual duplicates and the names are descriptive enough (e.g.: Title - Genre - Interpret - ... .mp3) to render false positives unlikely.
* So far, this script has only been tested in Linux, MacOS and Windows, but it could work on other Unix(-like) operating systems as well.
