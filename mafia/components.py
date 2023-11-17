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
class Alive:
    isAlive: bool = True

@component
class Saved:
    isSaved: bool = False



