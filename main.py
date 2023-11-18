import eloy
from mafia import systems as s

# This next line is overly specific because I want to make a working
# example but I don't want to mess with your organization. Feel free
# to change it.
from mafia.components import MafiaLose


def main():
    roleCounts = s.setRules()
    players = s.createPlayers(roleCounts)

    # Create an overarching "game_state" entity to hold global state data.
    game_state = eloy.create_entity
    # The "game_state" requires a "MafiaLose" component to track
    # whether the mafia have lost.
    # Other similar components would be added to track other pertinent
    # state information.
    eloy.add_component(game_state, MafiaLose())

    # Hook in the "mafiaLoseCheck" function to run immediately after
    # the backend finishes processing any incoming network data.
    eloy.set_handler(eloy.Stage.postNetwork, s.mafiaLoseCheck)


main()
