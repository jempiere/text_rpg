from ../eloy import *
from dataclasses import dataclass as component

@component
class mafia:
    mafia: bool = True

@component
class detective:
    detective: bool = True

@component
class angel:
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



