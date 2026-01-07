import pygame
from pygame import mixer
from time import sleep
from HelperScripts.Manage.Scene import *
import HelperScripts.Util as Util
import HelperScripts.GlobalVars as var
import HelperScripts.Manage.Sound.Music as music
import HelperScripts.Manage.Sound.Playlist as Playlist
from Start import Start

#Set Music quality
mixer.init() 
pygame.mixer.init(frequency=48000, size=-16, channels=1, buffer=1024)
# region Vars to not edit
var.ScreenSize = (pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
var.UpdateFrame = True
clock = pygame.time.Clock()
# endregion
 
def main():
    Util.Start() # starts other utility stuff such as music, and play time
    var.Parts = Start(var.screen) # start the whole game
    Playlist.AddFolder("Music",Name="Main")
    Playlist.Load("Main",Random=True)
    running = True
    # to add music do Music.Add() you can add a folder name or a sound file
    #music.Add("Music",Random=True)
    sleep(.1) #Fixes visule bugs
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #end event/ close window if the X button is pressed
                running = False
            if event.type == pygame.WINDOWRESIZED:
                var.ScreenSize = (pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
                var.UpdateFrame = True
        
        if var.UpdateFrame == True: #if need to add anything
            #var.screen.fill('black')
            var.screen.blit(*Group(*var.Parts))
            var.UpdateFrame = False
        #go to next frame
        pygame.display.flip()
        
        clock.tick(var.FPS)  # limit FPS

    pygame.quit()

if __name__ == "__main__":
    var.Parts = [[],[]]
    pygame.init()
    main()
    