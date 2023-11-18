from text_rpg import eloy
import components as c

def createPerson(Role = None):
    person = eloy.create_entity()
    if Role != None:
        eloy.add_component(person, Role)
    eloy.add_component(person, c.mafiaLose)
    eloy.add_component(person, c.isSaved)
    return person
#create a person and make them living

def createGameState():
    state = eloy.create_entity()
    eloy.add_component(state, c.isEnded)
    eloy.add_component(state, c.phase)
    return state
#create the game state and keep it running with the isEnded component, and the phase component.

def createNarrator():
    narrator = eloy.create_entity()
    eloy.add_component(narrator, c.responseDict)
#create the narrator and his dictionary of responses from the players.


