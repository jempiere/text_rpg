import esper
from dataclasses import dataclass
import curses
import threading

# stdscr = curses.initscr()


# @dataclass
# class Renderable:
#     visual: str


# @dataclass
# class Region:
#     identifier: str
#     height: int
#     width: int
#     corner: tuple
#     layer: int
#     renderable: int


# def render():
#     for region in esper.get_component(Region):
#         renderable = esper.component_for_entity(region.renderable, Renderable)
#         # TODO: Render stuff


def main(stdscr):
    stdscr.erase()

    window = curses.newwin(5, 5, 1, 1)

    window.box()
    # stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_REVERSE)
    # stdscr.refresh()
    # stdscr.getch()
    window.refresh()
    window.getch()


curses.wrapper(main)
