import HelperScripts.GlobalVars as var
from HelperScripts.Manage.Sound.Music import Add as MusicAdd
from pathlib import Path


def Load(Playlist, Random = False):
    Playlist = var.Playlists[1].index(Playlist)
    MusicAdd(*var.Playlists[0][Playlist], Random = Random)


def Add(*Song, Name = None):
    if Name == None:
        print("Error no name for playlist")
    else:
        var.Playlists[0].append([])
        var.Playlists[1].append(Name)
        PlaylistSpot = var.Playlists[1].index(Name)
        for Song in Song:
            var.Playlists[0][PlaylistSpot].append(Song)

def Remove(*args):
    for i in args:
        Del = var.Playlists[1].index(i)
        #list.remove(Var) deletes the item that is called Var from list
        #list.pop(numb) removes the list[numb] from the list and if no number givven removes the last value
        var.Playlists[0].pop(Del)
        var.Playlists[1].pop(Del)

def AddFolder(*Folder, Name = None):
    if Name == None:
        print("Error no name for playlist")
    else:
        songs = []
        for Folders in Folder:
            path = Path(Folders)
            if path.is_dir():
                for file in path.iterdir():
                    if file.is_file():
                        songs.append(str(file))
    Add(*songs,Name=Name)

def AddSong(*Song,Playlist = None):
    Playlist = var.Playlists[1].index(Playlist)
    for song in Song:
        var.Playlists[0][Playlist].append(song)

def RemoveSong(*Song,Playlist = None):
    Playlist = var.Playlists[1].index(Playlist)
    for song in Song:
        var.Playlists[0][Playlist].pop(song)
