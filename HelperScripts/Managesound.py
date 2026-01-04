import HelperScripts.GlobalVars as var

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



# endregion
