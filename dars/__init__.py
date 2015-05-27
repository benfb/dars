import sys
import subprocess
import argparse
import shutil
import pydub as pd

def detectFormat(fileName):
    """Get the extension of a file"""
    ext = fileName.split(".")[1]
    return ext

def instantiateSong(fileName, ext):
    """Create an AudioSegment with the data from the given file"""
    if(ext == "mp3"):
        return pd.AudioSegment.from_mp3(fileName)
    elif(ext == "wav"):
        return pd.AudioSegment.from_wav(fileName)
    elif(ext == "ogg"):
        return pd.AudioSegment.from_ogg(fileName)
    elif(ext == "flv"):
        return pd.AudioSegment.from_flv(fileName)
    else:
        return pd.AudioSegment.from_file(fileName, ext)

def findGap(song):
    """Return the position of silence in a song"""
    if(args.verbose):
        print("Scanning for silence in " + args.name + "...")
    silence = pd.silence.detect_silence(song)
    maxlength = 0

    for pair in silence:
        length = pair[1] - pair[0]
        if length >= maxlength:
            maxlength = length
            gap = pair

    return gap

def splitSong(songToSplit, start1, start2):
    """Split a song into two parts, one starting at start1, the other at start2"""
    songs = [songToSplit[:start1+2000], songToSplit[start2-2000:]]
    return songs

def saveFiles(fileName1, fileName2, songs):
    """Save songs to files"""
    outSongs = [fileName1, fileName2]
    songs[0].export(fileName1, format=fileName1.split(".")[1], tags={"album": args.album, "artist": args.artist})
    songs[1].export(fileName2, format=fileName2.split(".")[1], tags={"album": args.album, "artist": args.artist})
    return outSongs

def addToiTunes(fileName):
    """Attempts to add fileName to iTunes by moving it into the dfault Automatically Add to iTunes.localized folder"""
    try:
        shutil.move(fileName, "/Users/ben/Music/iTunes/iTunes Media/Automatically Add to iTunes.localized")
    except IOError:
        print("Failed to add song to iTunes: The file or folder doesn't exist!")

def parseArgs():
    """Parses arguments passed in via the command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="the file you want to split")
    parser.add_argument("out1", help="the name of the first file you want to output")
    parser.add_argument("out2", help="the name of the second file you want to output")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-i", "--itunes", help="attempt to add the split songs to iTunes", action="store_true")
    parser.add_argument("--artist", help="specifies artist for tagging of output files")
    parser.add_argument("--album", help="specifies album for tagging of output files")
    return parser.parse_args()

def main():
    """Actually runs the program"""
    songIn = instantiateSong(args.name, detectFormat(args.name))
    times = findGap(songIn)
    saveFiles(args.out1, args.out2, splitSong(songIn, times[0], times[1]))
    if(args.itunes):
        if(args.verbose):
            print("Adding " + args.out1 + " to iTunes...")
        addToiTunes(args.out1)
        if(args.verbose):
            print("Adding " + args.out2 + " to iTunes...")
        addToiTunes(args.out2)
    if(args.verbose):
        print "All done!"

args = parseArgs()