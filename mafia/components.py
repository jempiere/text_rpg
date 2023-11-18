from text_rpg import eloy
from eloy import component


@component
class GameStatus:
    gameOver: bool = False


@component
class Rules:
    mafiaCount: int = 0
    detectiveCount: int = 0

# This component should only be implemented once. It should be attached to
# a "game_state" entity or some similar entity which collects the global state
# information. I created this in `main`.
@component
class MafiaLose:
    mafiaLose: bool = False


@component
class Mafia:
    mafia: bool = True


@component
class Detective:
    detective: bool = True


@component
class Angel:
    angel: bool = True


@component
class Alive:  # Attribute for every player
    isAlive: bool = True


@component
class Saved:  # Attribute for every player
    isSaved: bool = False


@component
class Votes:  # Part of Narrator exclusively
    votes: dict = {}


@component
class Ballot:
    ballot: str = ""


@component
class Input:  # Everyone has this- used to check if they have voted or not.
    inputGiven: bool = False


@component
class VotingPhase:
    voting: bool = True  # phase where each user will mark who they are voting for.


@component
class DiscussionPhase:  # phase where each user will discuss
    discussion: bool = True


@component
class NightPhase:  # phase where the narrator summarizes the day.
    night: bool = True


@component
class MorningPhase:  # phase where the narrator explains who died/lived.
    morning: bool = True


@component
class InputPhase:  # phase where the mafia, detective, and angel give their input.
    inputting: bool = True

@component
class Roster:
    roster: list = []

@component
class RecentDeath: #this saves to the narrator the most recent death. Important for orchestration processes.
    recentDeath: str = ""


@component
class AngelSaved:
    angelSaved: bool = False
