import sys
import pydub as pd

def detectFormat(fileName):
    ext = fileName.split(".")[1]
    return ext

def instantiateSong(fileName, ext):
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
    print("Scanning for silence...")
    silence = pd.silence.detect_silence(song)
    maxlength = 0

    for pair in silence:
        length = pair[1] - pair[0]
        if length >= maxlength:
            maxlength = length
            gap = pair

    return gap

def splitSong(songToSplit, start1, start2):
    songs = [songToSplit[:start1+2000], songToSplit[start2-2000:]]
    return songs

def saveFiles(fileName1, fileName2, songs):
    songs[0].export(fileName1, format=fileName1.split(".")[1])
    songs[1].export(fileName2, format=fileName2.split(".")[1])

if __name__ == "__main__":
    name = sys.argv[1]
    out1 = sys.argv[2]
    out2 = sys.argv[3]
    songIn = instantiateSong(name, detectFormat(name))
    times = findGap(songIn)
    saveFiles(out1, out2, splitSong(songIn, times[0], times[1]))
