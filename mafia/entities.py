import eloy
from components import *

def createPerson(Role = None):
    person = eloy.create_entity()
    if Role != None:
        eloy.add_component(person, Role)
    eloy.add_component(person, isAlive)
    eloy.add_component(person, isSaved)
    return person
#create a person and make them living

def createGameState():
    state = eloy.create_entity()
    eloy.add_component(state, isEnded)
    eloy.add_component(state, phase)
    return person
#create the game state and keep it running with the isEnded component, and the phase component.

def createNarrator():
    narrator = eloy.create_entity()
    eloy.add_component(narrator, responseDict)
#create the narrator and his dictionary of responses from the players.


