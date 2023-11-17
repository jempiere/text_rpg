import eloy
from components important *

def createPerson(Role = None):
    person = esper.create_entity()
    if Role != None:
        esper.add_component(person, Role)
    esper.add_component(person, isAlive)
    esper.add_component(person, isSaved)
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


