from HelperScripts.Manage.Scene import *
import HelperScripts.Create_Shape as shape
from time import sleep
import socket
import pygame
import HelperScripts.GlobalVars as var
from pygame.time import Clock
from Test.BlockList import PlaceBlock,BlockArrya
clock = Clock()
HOST = "127.0.0.1"
PORT = 65432

PreString = ""
PreArray = []  # we'll initialize it after receiving world
toSent = []
Current_Block = "dirt"
CurrentBlockNumb = 0
MaxSize = len(BlockArrya)-1

import HelperScripts.GlobalVars as var


def Event(event):
    global toSent,Current_Block,CurrentBlockNumb,BlockArrya,MaxSize
    if event.type == pygame.MOUSEBUTTONUP:
        for Part in var.Parts[0]:
            if Part[1].collidepoint(event.pos):

                part_pos = int(Part[1].topleft[0]/100),int(Part[1].topleft[1]/100)
                if part_pos[1] <= 12:

                    toSent.append(f"{part_pos[0]},{part_pos[1]}|{Current_Block}\n")

    elif event.type == pygame.KEYDOWN:
        
        if event.key == pygame.K_e:

            CurrentBlockNumb += 1
            if CurrentBlockNumb == MaxSize+1:
                CurrentBlockNumb = 0
            
            Current_Block = BlockArrya[CurrentBlockNumb]

        elif event.key == pygame.K_q:
            CurrentBlockNumb -= 1
            if CurrentBlockNumb == -1:
                CurrentBlockNumb = MaxSize
            Current_Block = BlockArrya[CurrentBlockNumb]
        print (Current_Block)

def Server():
    global PreArray
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # create first world
        data = s.recv(4096).decode()
        ArrayWorld(data)
        PreArray = []
        fps = var.FPS
        while True:
            if len(toSent) >= 1:
                for Info in toSent:
                    s.sendall(Info.encode("utf-8"))
                toSent.clear()
            data = s.recv(4096).decode()
            if not data:
                break
            ArrayWorld(data)

def ArrayWorld(worldString):
    global PreArray
    fps = var.FPS
    worldArray = []
    clock.tick(fps*2)
    # Build world with colors

    # Build worldArray with raw block names
    worldArray = []
    for row_str in worldString.split("~"):
        row = row_str.split("|")
        worldArray.append(row)

    # Adjust PreArray to match world dimensions
    while len(PreArray) < len(worldArray):
        PreArray.append([])
    while len(PreArray) > len(worldArray):
        PreArray.pop()

    for y in range(len(worldArray)):
        while len(PreArray[y]) < len(worldArray[y]):
            PreArray[y].append([])
        while len(PreArray[y]) > len(worldArray[y]):
            PreArray[y].pop()
    
    # Update blocks if they changed
    for Y in range(len(worldArray)):
        for X in range(len(worldArray[Y])):
            if PreArray[Y][X] != worldArray[Y][X]:
                RemoveObject(f"Block{X},{Y}")
                PlaceBlock(X, Y, worldArray[Y][X])
                PreArray[Y][X] = worldArray[Y][X]

