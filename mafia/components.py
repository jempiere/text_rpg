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
class votingPhase:
    voting: bool = True

@component
class discussionPhase:
    discussion: bool = True

@component
class nightPhase:
    night: bool = True

@component
class morningPhase:
    morning: bool = True

@component
class inputPhase:
    inputting: bool = True
