#For documentation refer to my Github: https://github.com/Zylence/m3u-Playlist-Creation-Script
import os
from optparse import OptionParser
import music_tag

def scanDirectories():
    '''Scans 'startDirectory' and all subdirectories for all files listed in 'acceptedFormats' and
    writes them to a dictionary mapping files to a list of paths.
    '''
    foundFiles = dict()
    for root, dirs, files in os.walk(startDirectory):
        if os.path.split(root)[1] not in excludeDirectories:
            for file in files:
                if os.path.splitext(file)[1] in acceptedFormats:
                    foundFiles.setdefault(file, []).append(root)
    return foundFiles


def createPathsHelper(filename, path):
    '''Returns a pair of an absolute or relative path according to the'absolutePaths' variable
    and an absolute path used in case of adding #EXTINF.
    '''

    abs_path = os.path.join(path, filename)
    if absolutePaths:
        return abs_path, abs_path
    else:
        return os.path.relpath(abs_path, start=startDirectory), abs_path


def createPaths(files):
    '''Takes a dictionary of files mapping to paths. Returns a list of absolute or
    relative paths with duplicates either removed or not.
    '''

    resPaths = []
    for filename, paths in files.items():    # paths is a list
        if removeDuplicates:
            # discard all but the first path
            resPaths.append(createPathsHelper(filename, paths[0]))
        else:
            # keep all paths
            for path in paths:
                resPaths.append(createPathsHelper(filename, path))
    print(f'{len(resPaths)} files found in {startDirectory}.')
    return resPaths


def writePlaylist(paths):
    '''Writes all the 'paths' into a playlist file named 'fileName' using 'mode'
    as method of writing.
    '''

    with open(fileName, mode, encoding=codec) as f:
        for path, _ in paths:
            f.write(path + '\n')
        f.close()

def writePlaylistExt(paths):
    '''Writes all the 'paths' into a playlist file named 'fileName' using 'mode'
    as method of writing.
    also adds '#EXTINF:LENGTH, ARTIST - TRACK'
    '''

    with open(fileName, mode, encoding=codec) as f:
        f.write('#EXTM3U\n\n')
        for path, abs_path in paths:
            mt = music_tag.load_file(abs_path)
            length = int(round(mt['#length'].value))
            artist = mt['artist'].value
            track = mt['tracktitle'].value
            f.write(f'#EXTINF:{length},{artist} - {track}\n')
            f.write(path)
            f.write('\n\n')
        f.close()


if __name__ == '__main__':
    # args parsing
    parser = OptionParser()
    parser.add_option('-n', default='playlist.m3u',
                      help='the name of your playlist, use `.m3u` extension')
    parser.add_option('-m', default='w',
                      help='mode used for writing, choose `a` to append, and `w` to overwrite the playlist file')
    parser.add_option('-c', default='utf-8',
                      help='codec used for opening (writing) a file')
    parser.add_option('-s', default=os.getcwd(),
                      help='the starting directory for the script to scan for music files, usually your music library')
    parser.add_option('-e', default='',
                      help='string containing subdirectories separated by whitespaces, e.g.: `Celtic Classic` will '
                           'not be included in the playlist')
    parser.add_option('-d', action='store_true', default=False,
                      help='boolean determining whether or not to exclude duplicate files from the playlist')
    parser.add_option('-i', action='store_true', default=False,
                      help='boolean determining whether or not to include #EXTINF tag before each file')
    parser.add_option('-r', action='store_true', default=False,
                      help='boolean determining whether to use relative paths')
    parser.add_option('-f', default='.mp3 .flac .wav .aac',
                      help='string containing file formats separated by whitespaces, e.g.: `.mp3 .flac`')
    (options, args) = parser.parse_args()

    # if you prefer hard coding - edit those assignments
    fileName = options.n
    mode = options.m
    codec = options.c
    startDirectory = options.s
    excludeDirectories = options.e.split()
    removeDuplicates = options.d
    acceptedFormats = options.f.split()
    absolutePaths = not options.r
    appendExtInf = options.i

    # main script
    foundFiles = scanDirectories()
    paths = createPaths(foundFiles)
    if appendExtInf:
        writePlaylistExt(paths)
    else:
        writePlaylist(paths)
