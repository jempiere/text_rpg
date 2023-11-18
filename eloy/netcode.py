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
    print("about to get events")
    for msg in libp2py.get_events():
        print(msg)
    print("about to get messages")
    for msg in libp2py.get_messages():
        print(msg)
    print("about to test")
    libp2py.push_message("test")
    print("about to sleep")
    time.sleep(0.3)
