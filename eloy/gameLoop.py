# This file is the main game loop. It calls systems at the relevent times.
# It schedules our own code to run at the relevant times.

# TODO: detect dropped hosts
# TODO: call esper.process at some point. required for various esper methods.

import esper


class Stage:
    preNetwork = "preNetwork"
    postNetwork = "postNetwork"
    preRender = "preRender"
    postRender = "postRender"


def gameLoop():
    # Pre network
    esper.dispatch_event("preNetwork")

    # Network
    # (our code)

    # Pre render
    esper.dispatch_event("postNetwork")
    esper.dispatch_event("preRender")

    # Render
    # (our code)

    # Post render
    esper.dispatch_event("postRender")
