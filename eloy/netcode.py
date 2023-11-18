import esper
from dataclasses import dataclass, field
from typing import List
import libp2py
import time

libp2py.init("myapp")


@dataclass
class PlayersList:
    players: list = field(
        default_factory=list
    )  # TODO: IMPORTANT: In Python 3.12 wait nvm


while True:
    for msg in libp2py.get_events():
        print(msg)
    libp2py.upload_bugger("test")
    time.sleep(0.1)
