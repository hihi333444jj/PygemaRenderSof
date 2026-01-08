import pygame
from pygame import mixer
from time import sleep
from HelperScripts.Manage.Scene import *
import HelperScripts.Create_Shape as shape
import HelperScripts.Util as Util
import HelperScripts.GlobalVars as var
import HelperScripts.Manage.Sound.Music as Music
import HelperScripts.Manage.Sound.Playlist as Playlist
from Start import Start
import Credits as CCredits
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
    running = True
    Music.Add("Music")
    # to add music do Music.Add() you can add a folder name or a sound file
    #music.Add("Music",Random=True)
    sleep(.1) #Fixes visule bugs
    Credets = shape.Label("Credits",290,340,50,(255,255,255),rotateAngle=45)
    AddObject([Credets, "Credits"])
    print(var.Parts)
    DisplayCredits = False
    cred = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #end event/ close window if the X button is pressed
                running = False
            if event.type == pygame.WINDOWRESIZED:
                var.ScreenSize = (pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
                var.UpdateFrame = True
            elif DisplayCredits:
                if event.type == pygame.MOUSEBUTTONUP:
                    CCredits.HandleClicks(event.pos)
                elif event.type == pygame.MOUSEWHEEL:
                    CCredits.HandleScroll(event)
            if event.type == pygame.MOUSEBUTTONUP:
                if Credets[1].collidepoint(event.pos):
                    if DisplayCredits == False:
                        DisplayCredits = True
                        cred = CCredits.Run()
                    else:
                        print(len(cred))
                        for i in range(0,len(cred)):
                            print(cred[0])
                            DisplayCredits = False
                            DeleteObject(cred[0])
                            cred.pop(0)
        if var.UpdateFrame == True: #if need to add anything
            #var.screen.fill('black')
            var.screen.blit(*Group(*var.Parts))
            var.UpdateFrame = False
            #var.screen.blit(*Credets)
        #go to next frame
        pygame.display.flip()
        
        clock.tick(var.FPS)  # limit FPS

    pygame.quit()

if __name__ == "__main__":
    var.Parts = [[],[]]
    pygame.init()
    main()
    