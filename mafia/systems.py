from eloy import *

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
        savedComponent.isSaved = False
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
