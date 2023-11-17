from ../eloy import *
from dataclasses import dataclass as component

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
class Alive:                # Attribute for every player
    isAlive: bool = True

@component
class Saved:                # Attribute for every player
    isSaved: bool = False

@component
class Votes:                # Part of Narrator exclusively
    votes: dict = {}

@component
class Input:                # Everyone has this- used to check if they have voted or not.
    inputGiven: bool = False

@component
class votingPhase:
    voting: bool = True # phase where each user will mark who they are voting for.

@component
class discussionPhase: #phase where each user will discuss
    discussion: bool = True

@component
class nightPhase: #phase where the narrator summarizes the day.
    night: bool = True

@component
class morningPhase: #phase where the narrator explains who died/lived.
    morning: bool = True

@component
class inputPhase: #phase where the mafia, detective, and angel give their input.
    inputting: bool = True
