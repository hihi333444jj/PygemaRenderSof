import HelperScripts.GlobalVars as var
from pygame import mixer
from time import sleep
# region Sound

def AddSound(*args): #input object then name so [rect(args), "rectangle"]
    for i in args:
        var.Sounds[0].append(i[0])
        var.Sounds[1].append(i[1])
    var.UpdateFrame = True

def DeleteSound(*args):
    for i in args:
        Del = var.Sounds[1].index(i)
        #list.remove(Var) deletes the item that is called Var from list
        #list.pop(numb) removes the list[numb] from the list and if no number givven removes the last value
        var.Sounds[0].pop(Del)
        var.Sounds[1].pop(Del)
def Music():
    pos = 0
    mixer.music.load("Music/Ado_Show.mp3")
    mixer.music.play(loops=0, start=0.0, fade_ms = 0)
    while True:
        if len(var.Music) == 0:
            sleep(.1)
        else:
            if pos >= len(var.Music):
                pos = 0
            else:
                pos += 1
            mixer.music.load(var.Music[pos])
            print(mixer.Sound.get_length(var.Music[pos]))
            sleep(mixer.Sound.get_length(var.Music[pos]))


# endregion
