#from ../eloy import *
import importlib
import random
import entities as ent

eloy = importlib.import_module('eloy')

def AssignPlayers():
    players = [0,1,2,3]
    for p in players:
        v = random.randint(0,4)
        if v == 0:
            #player is mafia
            p = ent.createPerson(eloy.get_component(Mafia))
            ...
        elif v == 1:
            #player is detective
            ...
        elif v == 2:
            #player is angel
            ...
        elif v == 3:
            #player has No Role