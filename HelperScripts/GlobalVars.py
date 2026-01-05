import pygame
#screen = pygame.display.set_mode((1920, 1200),pygame.RESIZABLE)
ScreenSize = (400, 400)
screen = pygame.display.set_mode(ScreenSize,pygame.RESIZABLE)
Parts = []
Sounds =  [] #sounds that are currently playing
MusicPlaylists = []# this will store [playlist,[CurrentPlaylist,CurrentSong]] playlist is just an array of sound files
PartsOri = []
FPS = 60
CurrentFps = 0
CurrentSec = 0
CurrentMin = 0
CurrentHr = 0
UpdateFrame = False
detail = 1
GravObjects = [] #Object[Name,Vl[X,Y],bounce,offset]