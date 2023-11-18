import eloy
from mafia import systems as s
from mafia import components as c

# This next line is overly specific because I want to make a working
# example but I don't want to mess with your organization. Feel free
# to change it.
from mafia.components import MafiaLose


def main():
    roleCounts = s.setRules() # Defines how many Mafia and Detectives
    players = s.createPlayers(roleCounts) # creates entities with roles assigned

    # Create an overarching "game_state" entity to hold global state data.
    gameState = eloy.create_entity
    eloy.add_component(gameState, c.Roster)
    playerList = eloy.component_for_entity(gameState, c.Roster)
    playerList.roster = players
    # The "game_state" requires a "MafiaLose" component to track
    # whether the mafia have lost.
    # Other similar components would be added to track other pertinent
    # state information.
    eloy.add_component(gameState, MafiaLose())

    # Hook in the "mafiaLoseCheck" function to run immediately after
    # the backend finishes processing any incoming network data.
    eloy.set_handler(eloy.Stage.postNetwork, s.mafiaLoseCheck)


main()
