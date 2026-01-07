import pygame
ScreenSize = (400, 400)
FPS = 60



# region You do not need to change past here...
Parts = []
screen = pygame.display.set_mode(ScreenSize,pygame.RESIZABLE)
Sounds =  [] #sounds that are currently playing
MusicPlaylist = []
Playlists = [[],[]] # this will store [playlist,Name] playlist is just an array of sound files
PartsOri = []
CurrentFps = 0
CurrentSec = 0
CurrentMin = 0
CurrentHr = 0
UpdateFrame = False
GravObjects = [] #Object[Name,Vl[X,Y],bounce,offset]
# endregion