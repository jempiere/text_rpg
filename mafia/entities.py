from ../eloy import esper
from components important *

def createPerson():
    person = esper.create_entity()
    esper.add_component(person, isAlive)
    return person
#create a person and make them living

def createGameState():
    state = esper.create_entity()
    esper.add_component(state, isEnded)
    esper.add_component(state, phase)
    return person
#create the game state and keep it running with the isEnded component, and the phase component.

def createNarrator():
    narrator = esper.create_entity()
    esper.add_component(narrator, responseDict)
#create the narrator and his dictionary of responses from the players.

def createTimer():
    timer = esper.create_entity()
    esper.add_component(timer, clock)
#create a timer entity for the discussion phase.


