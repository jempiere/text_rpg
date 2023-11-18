import eloy
from mafia import systems as s
from mafia import components as c
#from mafia.components import MafiaLose

world = 0
    
# main() is meant to only be run once to instantiate the game state for the duration of one game.
def main():
    roleCounts = s.setRules() # Defines how many Mafia and Detectives
    players = s.createPlayers(roleCounts) # creates entities with roles assigned

    # Create an overarching "game_state" entity to hold global state data.
    gameState = eloy.create_entity
    eloy.add_component(gameState, c.Roster)
    playerList = eloy.component_for_entity(gameState, c.Roster)
    playerList.roster = players

    eloy.add_component(gameState, c.Rules)  # Stores how many mafia and detectives are in this instance of mafia game
    rules = eloy.component_for_entity(gameState, c.Rules)
    rules.mafiaCount = roleCounts[0]
    rules.detectiveCount = roleCounts[1]

    eloy.add_component(gameState, c.NightPhase)
    eloy.add_component(gameState, c.GameStatus) # Component that will decide when the game is over
    eloy.add_component(gameState, c.MafiaLose)  # The "game_state" requires a "MafiaLose" component 
    world = gameState
                                                # to track whether the mafia have lost.

    # Hook in the "mafiaLoseCheck" function to run immediately after
    # the backend finishes processing any incoming network data.
    #eloy.set_handler(eloy.Stage.postNetwork, s.mafiaLoseCheck()) # <---- THIS PROBABLY SHOULD GO IN SYSTEMS.PY


main()
