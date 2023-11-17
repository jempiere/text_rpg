import esper
from dataclasses import dataclass, Field
from typing import List


@dataclass
class PlayersList:
    players: list = Field(
        default_factory=list
    )  # TODO: IMPORTANT: In Python 3.12 wait nvm
