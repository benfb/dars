import sys
import argparse
import shutil
import pydub as pd

def detectFormat(fileName):
    """Get the extension of a file"""
    ext = fileName.split(".")[1]
    return ext

def instantiateSong(fileName):
    """Create an AudioSegment with the data from the given file"""
    ext = detectFormat(fileName)
    if(ext == "mp3"):
        return pd.AudioSegment.from_mp3(fileName)
    elif(ext == "wav"):
        return pd.AudioSegment.from_wav(fileName)
    elif(ext == "ogg"):
        return pd.AudioSegment.from_ogg(fileName)
    elif(ext == "flv"):
        return pd.AudioSegment.from_flv(fileName)
    elif(ext == "m4a"):
        return pd.AudioSegment.from_file(fileName, "mp4")
    else:
        return pd.AudioSegment.from_file(fileName, ext)

def findGap(song):
    """Return the position of silence in a song"""
    try:
        silence = pd.silence.detect_silence(song)
    except IOError:
        print("There isn't a song there!")

    maxlength = 0

    for pair in silence:
        length = pair[1] - pair[0]
        if length >= maxlength:
            maxlength = length
            gap = pair

    return gap

def splitSong(songToSplit, start1, start2):
    """Split a song into two parts, one starting at start1, the other at start2"""
    print "start1 " + str(start1)
    print "start2 " + str(start2)
    # songs = [songToSplit[:start1+2000], songToSplit[start2-2000:]]
    songs = [songToSplit[:start1], songToSplit[start2:]]
    return songs

def saveFiles(fileName1, fileName2, songs):
    """Save songs to files"""
    songs[0].export(fileName1, format=detectFormat(fileName1))
    songs[1].export(fileName2, format=detectFormat(fileName2))

def saveFiles(fileName1, fileName2, songs, artist, album, trackNum):
    """Save songs to files"""
    songs[0].export(fileName1, format=detectFormat(fileName1), tags={'artist': artist, 'album': album, 'track': trackNum})
    songs[1].export(fileName2, format=detectFormat(fileName2), tags={'artist': artist, 'album': album, 'track': str(int(trackNum) + 1)})

def trackSeek(path, artist, album, track, trackNum, fmt):
    """Actually runs the program"""
    hiddenName = "(Hidden Track).{}".format(fmt)
    trackName = track + ".{}".format(fmt)
    songIn = instantiateSong(path)
    times = findGap(songIn)
    saveFiles(trackName, hiddenName, splitSong(songIn, times[0], times[1]), artist, album, trackNum)
    # return [path, track.rsplit('/',1)[0] +'/{}'.format(hiddenName)]
    return [trackName, hiddenName]

def parseArgs():
    """Parses arguments passed in via the command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="the file you want to split")
    parser.add_argument("out1", help="the name of the first file you want to output")
    parser.add_argument("out2", help="the name of the second file you want to output")
    return parser.parse_args()

if __name__ == '__main__':
    """Actually runs the program"""
    args = parseArgs()
    songIn = instantiateSong(args.name)
    times = findGap(songIn)
    saveFiles(args.out1, args.out2, splitSong(songIn, times[0], times[1]))
