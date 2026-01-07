import HelperScripts.GlobalVars as var
from pygame import mixer
from time import sleep
from pathlib import Path
from random import randint
# region Music
def Randomise(Playlist = None):
    if Playlist == None:
        MusicToAdd = var.MusicPlaylist
        MusicOrderNew = []
        for i in range(0,len(var.MusicPlaylist)):
            rand = randint(0,len(MusicToAdd)-1)
            MusicOrderNew.append(MusicToAdd[rand])
            MusicToAdd.pop(rand)
        var.MusicPlaylist = MusicOrderNew
def Add(*musics,Random=False):
    for item in musics:
        path = Path(item)

        if path.is_dir():
            for file in path.iterdir():
                if file.is_file():
                    var.MusicPlaylist.append(str(file))

        elif path.is_file():
            var.MusicPlaylist.append(str(path))
    if Random == True:
        Randomise()
    print("music",var.MusicPlaylist)

def Remove(*args):
    for i in args:
        var.MusicPlaylist.index(i)

def Music():
    pos = -1
    while True:
        if len(var.MusicPlaylist) == 0:
            sleep(.1)
        else:
            if pos >= len(var.MusicPlaylist):
                pos = 0
            else:
                pos += 1
            mixer.music.load(var.MusicPlaylist[pos])
            mixer.music.play(loops=0, start=0.0, fade_ms = 5000)
            song = var.MusicPlaylist[pos]
            sound = mixer.Sound(song)
            length = sound.get_length()
            print(length)
            sleep(length-1)


# endregion
