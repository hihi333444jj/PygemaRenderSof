import HelperScripts.GlobalVars as var
from HelperScripts.ManageScene import AddObject,Group,DeleteObject
from HelperScripts.Create_Shape import Rect
from itertools import product
import pygame
import threading
import numpy as np
# region Vars
GS = [4,4]
CGS = [10,10] #compressed grid size for less lag
# endregion 

# region Setup helper vars
SAND_COLOR = (212,201,0)
AIR_COLOR = (255,255,255)
GridPixels = []
pendingupdate = []
clock =  pygame.time.Clock()
GridSize = [int(var.ScreenSize[0]/GS[0]),int(var.ScreenSize[1]/GS[1])]
width, height = GridSize
GridPixelValue = np.full((width, height), 0, dtype=object)
to_remove = set()
to_add = set()
ActivePixels = set() #tuples work better becuse it will become very large
# endregion

# region helper defs
def idx(x, y): #this converts X,Y into a 2d array
    global height
    return (x * height + y)

def GetCGPos(X,Y):
    return(X//CGS[0],Y//CGS[1])
def GetColor(Type):
    if Type == 1:
        return(212,201,0)
    return(255,255,255)
def CGUpdate(x,y):
    Grid = []
    for cx in range(CGS[0]):
        GridX = x * CGS[0] + cx
        for cy in range(CGS[1]):
            GridY = y * CGS[1] + cy
            idx_flat = GridX * height + GridY
            Grid.append(GridPixels[idx_flat])
    DeleteObject(f"{x},{y}")
    AddObject([Group(*Grid),f"{x},{y}"])
# endregion

# region Main defs
def GenGrid():
    global width,height,GS,GridPixels,CGS
    GridPixels = []

    for x, y in product(range(width), range(height)):
        GridPixels.append(
            Rect(
                x * GS[0], y * GS[1],
                GS[0], GS[1],
                (255, 255, 255)
            )
        )

    for x in range(0, width, CGS[0]):
        for y in range(0, height, CGS[1]):
            cells = []
            for cx in range(CGS[0]):
                for cy in range(CGS[1]):
                    gx = x + cx
                    gy = y + cy

                    if gx < width and gy < height:
                        cells.append(GridPixels[idx(gx, gy)])

            if len(cells) == CGS[0] * CGS[1]:
                #clock.tick(100)
                AddObject([
                    Group(*cells),
                    f"{x//CGS[0]},{y//CGS[1]}"
                ])
    
def CreateSandEveryFPS():
    fps = var.FPS
    while True:
        clock.tick(fps)
        pos = (22,22)   
        GridPixelValue[pos[0],pos[1]] = 1
        GridPixels[idx(*pos)] = Rect(
            pos[0] * GS[0], pos[1] * GS[1],
            GS[0], GS[1],
            SAND_COLOR
        )
        if pos not in to_add:
            to_add.add(pos)
        CGSpos = GetCGPos(*pos)
        if tuple(CGSpos) not in pendingupdate:
            pendingupdate.append(tuple(CGSpos))
        if tuple(CGSpos) not in pendingupdate:
            pendingupdate.append(tuple(CGSpos))
        
     
def GravMove(wat,where,type,color):
    global pendingupdate
    #clear old sand
    GridPixelValue[wat[0],wat[1]] = 0
    #GridPixels[idx(wat[0] * GS[0], wat[1] * GS[1])].color = GetColor("Sand")
    GridPixels[idx(*wat)][0].fill(AIR_COLOR)

    #set new type
    x, y = where
    GridPixelValue[x,y] = type
    GridPixels[idx(x, y)][0].fill(SAND_COLOR)
    #remove old active pixle and add new
    to_remove.add(wat)
    to_add.add((x, y))
    #update frame
    CGpos = GetCGPos(x, y)
    pendingupdate.append(tuple(CGpos))

def Physics():
    fps = var.FPS
    while True:
        clock.tick(fps)
        
        for pos in ActivePixels:
            x, y = pos
            if GridPixelValue[x,y] == 1:
                if y < height - 1:
                    # try to move down
                    if GridPixelValue[x,y+1] == 0:
                        GravMove(pos, (x, y+1), 1,SAND_COLOR)
                    else:
                        for dx in [0, -1, 1]:
                            nx = x + dx
                            ny = y + 1
                            if 0 <= nx < width and GridPixelValue[nx][ny] == 0:
                                GravMove(pos, (nx, ny), 1,SAND_COLOR)
                                break

                else:
                    to_remove.add(pos)
        for Remove in to_remove:
            ActivePixels.discard(Remove)
        for Add in to_add:
            ActivePixels.add(Add)
        to_remove.clear()
        to_add.clear()
        
        
# endregion
def redraw():
    fps = var.FPS
    while True:
        clock.tick(fps)
        for pos in np.unique(pendingupdate, axis=0): 
            CGUpdate(*pos)
        pendingupdate.clear()
print("starting sand game")
print(GridSize)

t = threading.Thread(target=GenGrid)
t.start()
t.join()
CSE = threading.Thread(target=CreateSandEveryFPS, daemon=True)
CSE.start()
Phy = threading.Thread(target=Physics, daemon=True)
Phy.start()
UpdateScreen = threading.Thread(target=redraw, daemon=True)
UpdateScreen.start()

