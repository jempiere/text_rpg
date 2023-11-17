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
class Alive:
    isAlive: bool = True

@component
class Saved:
    isSaved: bool = False


    