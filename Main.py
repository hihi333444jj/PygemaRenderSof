import pygame
from HelperScripts.ManageScene import *
from HelperScripts.Util import StartAll
import HelperScripts.GlobalVars as var

from pygame import mixer
import HelperScripts.ManageMusic as music
mixer.init() 
#Set File quality
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

if __name__ == "__main__":
    pygame.init()
def app():
    return

def main():

    StartAll()
   
    clock = pygame.time.Clock()
    running = True
    #Start(screen)
    var.ScreenSize = (pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
    var.UpdateFrame = True
    #var.GravObjects = [[['ball'],[25,1],.9,[55,55]]]
    # to add music do Music.Add() you can add a folder name or a sound file
    while running:
        #var.UpdateFrame = True
        #Move(['sky', 'sun', 'background', 'tree','shop'],(1,1))
        #Max = max(pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
        #Line(random.randint(1,Max),random.randint(1,Max),random.randint(1,Max),random.randint(1,Max),RandomGradient(20,50,"right"),10, render=True)
        
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
    main()
    