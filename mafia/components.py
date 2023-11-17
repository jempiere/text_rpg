from ../eloy import *
from dataclasses import dataclass as component

@component
class mafia:
    ...

@component
class detective:
    ...

@component
class angel:
    ...



@component
class Alive:                # Attribute for every player
    isAlive: bool = True

@component
class Saved:                # Attribute for every player
    isSaved: bool = False

@component
class Votes:                # Part of Narrator exclusively
    votes: dict = {} 


    