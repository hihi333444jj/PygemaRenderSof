import HelperScripts.GlobalVars as var
from HelperScripts.ManageScene import AddObject,Group,DeleteObject
from HelperScripts.Create_Shape import Rect
import pygame
import threading
import math
from time import sleep
from random import randint

# region Vars
GS = [4,4]
CGS = [10,10] #compressed grid size for less lag
# endregion 

pendingupdate = []
# region Setup helper vars
GridPixels = []
GridPixelValue = []
clock =  pygame.time.Clock()
GridSize = [int(var.ScreenSize[0]/GS[0]),int(var.ScreenSize[1]/GS[1])]
width, height = GridSize
ActivePixels = []
# endregion

# region helper defs
def idx(x, y): #this converts X,Y into a 2d array
    global height
    return (x * height + y)

def GetCGPos(X,Y):
    return(math.floor(X/CGS[0]),math.floor(Y/CGS[1]))
def GetColor(Type):
    if Type == "Sand":
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
    global width,height,GS,GridPixels,GridPixelValue,CGS
    GridPixels = []

    for x in range(width):
        for y in range(height):
            GridPixelValue.append("Air")
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
    while True:
        clock.tick(100)
        pos = (20,20)
        GridPixelValue[idx(*pos)] = "Sand"
        GridPixels[idx(*pos)] = Rect(
            pos[0] * GS[0], pos[1] * GS[1],
            GS[0], GS[1],
            GetColor("Sand")
        )
        CGSpos = GetCGPos(*pos)
        try:
            ActivePixels.index([pos[0],pos[1]])
        except:
            ActivePixels.append([pos[0],pos[1]])
        CGUpdate(*CGSpos)
        

            
def GravMove(wat,where,type):
    global pendingupdate
    #clear old sand
    GridPixelValue[idx(*wat)] = "Air"
    GridPixels[idx(*wat)] = Rect(
        wat[0] * GS[0], wat[1] * GS[1],
        GS[0], GS[1],
        GetColor("Air")
    )
    #set new type
    GridPixelValue[idx(where[0], where[1]+1)] = type
    GridPixels[idx(where[0], where[1]+1)] = Rect(
        where[0] * GS[0], (where[1]+1) * GS[1],
        GS[0], GS[1],
        GetColor(type)
    )
    #remove old active pixle and add new
    ActivePixels.remove(wat)
    new_pos = [where[0], where[1]+1]
    ActivePixels.append(new_pos)
    #update frame
    try:
        pendingupdate.index([*GetCGPos(*new_pos)])
    except:
        pendingupdate.append([*GetCGPos(*new_pos)])

def Physics():
    
    while True:
        clock.tick(240)
        for pos in ActivePixels.copy():
            x, y = pos
            if GridPixelValue[idx(x, y)] == "Sand":
                if y < height - 1:
                    # try to move down
                    if GridPixelValue[idx(x, y+1)] == "Air":
                        GravMove(pos, [x, y], "Sand")
                    else:
                        left_free = x-1 >= 0 and GridPixelValue[idx(x-1, y+1)] == "Air"
                        right_free = x+1 < width and GridPixelValue[idx(x+1, y+1)] == "Air"
                        if left_free and right_free:
                            if randint(0,1) == 0:
                                GravMove(pos, [x-1, y], "Sand")
                            else:
                                GravMove(pos, [x+1, y], "Sand")
                        elif left_free:
                            GravMove(pos, [x-1, y], "Sand")
                        elif right_free:
                            GravMove(pos, [x+1, y], "Sand")
                        else:
                            ActivePixels.remove(pos)
                else:
                    ActivePixels.remove(pos)
        for UpdateNext in pendingupdate:
            CGUpdate(*UpdateNext)

        



# endregion











print("starting sand game")
print(GridSize)

t = threading.Thread(target=GenGrid)
t.start()
t.join()
CSE = threading.Thread(target=CreateSandEveryFPS, daemon=True)
CSE.start()
Phy = threading.Thread(target=Physics, daemon=True)
Phy.start()