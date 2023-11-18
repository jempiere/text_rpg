from text_rpg import eloy
import importlib
import random
import entities as ent
import components as c


# This system will be scheduled to run right after the backend
# finishes processing any incoming network data.
# This way, if the "host" has information about the mafia losing,
# our client will be updated before we test for it.
def mafiaLoseCheck():
    # Loop over every (entity, MafiaComponent) pair in the game.
    for ent, maf in eloy.get_component(c.Mafia):
        # Retrieve that entity's "Alive" component.
        # Note, this will error if the entity doesn't exist
        # or doesn't have an Alive component.
        alive = eloy.component_for_entity(ent, c.Alive)
        if alive.isAlive == True:
            # If any mafia are still alive, do nothing.
            return
    # If we get here, there are no mafia alive.
    # Get the list of all entities with a MafiaLose component.
    # This should be exactly one, created in `main`, unless you game developers
    # have made a mistake.
    # Get the [0] item from the returned list.
    ent, mafiaLose = eloy.get_component(c.MafiaLose)[0]
    # Now, the "game_state" entity will mark that the game is over.
    mafiaLose.mafiaLose = True


def setRules():
    users = [0, 1, 2, 3]  # PLACEHOLDER
    if len(users) < 4:
        ...
    elif 4 <= len(users) <= 6:
        mafia_count = 1
        detective_count = 1
    elif 7 <= len(users) <= 11:
        mafia_count = 2
        detective_count = 1
    elif 12 <= len(users) <= 15:
        mafia_count = 3
        detective_count = 2
    return (mafia_count, detective_count)


def createPlayers(roleCounts):
    mCount = 0  # mafia counter
    dCount = 0  # detective counter
    aCount = 0  # angel counter
    cCount = 0  # civilian counter
    users = [0, 1, 2, 3]
    players = []
    for i in range(len(users)):
        isValid = False
        while not isValid:
            v = random.randint(0, 4)
            if v == 0 and mCount < roleCounts[0]:
                isValid = True
            elif v == 1 and dCount < roleCounts[1]:
                isValid = True
            elif v == 2 and aCount < 1:
                isValid = True
            elif v == 3 and cCount < (len(users)-(roleCounts[0]+roleCounts[1])):
                isValid = True
        if v == 0:
            # player is mafia
            p = ent.createPerson(eloy.get_component(c.Mafia))
            mCount += 1
            ...
        elif v == 1:
            # player is detective
            p = ent.createPerson(eloy.get_component(c.Detective))
            dCount += 1
            ...
        elif v == 2:
            # player is angel
            p = ent.createPerson(eloy.get_component(c.Angel))
            aCount += 1
            ...
        elif v == 3:
            # player has no role
            cCount += 1
            ...
        players.append(p)
    return players


def changePhase(state):  # increment the phase
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


def killPlayer(
    player,
):  # set a single player's Alive to false, if their Saved is false.
    savedComponent = eloy.component_for_entity(player, c.Saved)
    if savedComponent.isSaved == False:
        aliveComponent = eloy.component_for_entity(player, c.Alive)
        aliveComponent.isAlive = False
        return True
    else:
        return False


def savePlayer(player):  # set Saved to True
    person = eloy.component_for_entity(player, c.Saved)
    person.isSaved = True
    return True


def investigatePlayer(player):
    if eloy.has_component(player, c.Mafia):
        return True
    else:
        return False


def resetSavedPlayer(allPlayers):  # reset all players Saved component.
    for player in allPlayers:
        savedComponent = eloy.component_for_entity(player, c.Saved)
        savedComponent.isSaved = False
    return True


def mostVotes(narrator):  # count all votes in the response dictionary.
    votesComponent = eloy.component_for_entity(narrator, c.Votes)
    greatest = 0
    greatestKey = ""
    for vote in votesComponent.votes:
        if votesComponent.votes[vote] > greatest:
            greatest = votesComponent.votes[vote]
            greatestKey = vote
    return (greatest, greatestKey)


def generateNarratorDict(
    narrator, allPlayers
):  # create the narrator's dictionary of players at the beginning of the game.
    dictComponent = eloy.component_for_entity(narrator, c.Votes)
    narratorDict = dictComponent.votes
    for player in allPlayers:
        narratorDict[player] = 0
    return True


def getVote(narrator, choice):  # add a player's vote to the narrator's dictionary
    dictComponent = eloy.component_for_entity(narrator, c.Votes)
    narratorDict = dictComponent.votes
    narratorDict[choice] += 1
    return True


def tallyVotes(
    narrator, allPlayers
):  # call getVote() over and over to move all votes from the players to the narrator's dictionary of responses.
    for player in allPlayers:
        playerChoice = eloy.component_for_entity(player, c.Ballot)
        playerChoice = playerChoice.ballot
        getVote(narrator, choice)
    return True


def removeVote(player):
    playerChoice = eloy.component_for_entity(player, c.Ballot)
    playerChoice = playerChoice.ballot
    playerChoice = ""
    return True


def removeVotes(allPlayers):
    for player in allPlayers:
        removeVote(player)
    return True
