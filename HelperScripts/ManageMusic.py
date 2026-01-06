import HelperScripts.GlobalVars as var
from pygame import mixer
from time import sleep
from pathlib import Path

# region Music
def Add(*args):
    for item in args:
        path = Path(item)

        if path.is_dir():
            for file in path.iterdir():
                if file.is_file():
                    var.MusicPlaylist.append(str(file))

        elif path.is_file():
            var.MusicPlaylist.append(str(path))
    print(var.MusicPlaylist)
def Music():
    pos = 0
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
