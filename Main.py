import pygame
from pygame import mixer
from time import sleep
from HelperScripts.Manage.Scene import *
import HelperScripts.Create_Shape as shape
import HelperScripts.Util as Util
import HelperScripts.GlobalVars as var
import HelperScripts.Manage.Sound.Music as Music
import HelperScripts.Manage.Sound.Playlist as Playlist
from Test.Blocks import Server, Event
#Set Music quality
mixer.init() 
pygame.mixer.init(frequency=48000, size=-16, channels=1, buffer=1024)
# region Vars to not edit
var.ScreenSize = (pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
var.UpdateFrame = True
clock = pygame.time.Clock()
# endregion
 
def main():
    import Start
    Util.Start() # starts other utility stuff such as music, and play time
    var.Parts = Start.Start(var.screen) # start the whole game
    #import SandGame
    #t = threading.Thread(target=Server, daemon=True)
    #t.start()
    running = True
    Music.Add("Music")

    sleep(.1)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #end event/ close window if the X button is pressed
                running = False
            if event.type == pygame.WINDOWRESIZED:
                var.ScreenSize = (pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
                var.UpdateFrame = True
            Start.Event(event)
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
    