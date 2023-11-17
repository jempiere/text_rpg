from eloy import *
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
            #player has no role
            ...

def changePhase(state=globalState): #increment the phase
    if eloy.has_component(state, morningPhase):
        eloy.remove_component(state, morningPhase)
        eloy.add_component(state, discussionPhase)
    elif eloy.has_component(state, discussionPhase):
        eloy.remove_component(state, discussionPhase)
        eloy.add_component(state, votingPhase)
    elif eloy.has_component(state, votingPhase):
        eloy.remove_component(state, votingPhase)
        eloy.add_component(state, nightPhase)
    elif eloy.has_component(state, nightPhase):
        eloy.remove_component(state, nightPhase)
        eloy.add_component(state, inputPhase)
    elif eloy.has_component(state, inputPhase):
        eloy.remove_component(state, inputPhase)
        eloy.add_component(state, morningPhase)

def killPlayer(player): #set a single player's Alive to false, if their Saved is false.
    savedComponent = eloy.component_for_entity(player, Saved)
    if savedComponent.isSaved == False:
        aliveComponent = eloy.component_for_entity(player, Alive)
        aliveComponent.isAlive = False
        return True
    else:
        return False

def savePlayer(player): #set Saved to True
    person = eloy.component_for_entity(player, Saved)
    person.isSaved = True
    return True

def investigatePlayer(player):
    if eloy.has_component(player, mafia):
        return True
    else:
        return False

def resetSavedPlayer(allPlayers):
    for player in allPlayers:
        savedComponent = eloy.component_for_entity(player, Saved)
        savedComponent.isSaved = False
    return True
