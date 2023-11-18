
from dataclasses import dataclass
@dataclass
class Renderable:
    visual: str

@dataclass
class Region:
    identifier: str
    height: int
    width : int
    corner : tuple
    renderable : int


import threading
import curses

import rich

import sys
import io


testme =\
"""$b0$f7░░░░░░░░░░░░░░▄▄▄▄▄▄▄▄▄▄▄▄░░░░░░░░░░░░░░$fd$bd
$b0$f7░░░░░░░░░░░░▄████████████████▄░░░░░░░░░░$fd$bd      Nicholas cage admonishes you to not commit this $f1$suMURDER$fd$sd.
$b0$f3░░░░░░░░░░▄██▀░░░░░░░▀▀████████▄░░░░░░░░$fd$bd
$b0$f1░░░░░░░░░▄█▀░░░░░░░░░░░░░▀▀██████▄░░░░░░$fd$bd
$b0$f1░░░░░░░$b2░░███▄░░░░░░░$b0░░░░░░░░▀██████░░░░░$fd$bd
$b0$f1░░░░░░░░▄░░▀▀█░░░░░░░░░░░░░░░░██████░░░░$fd$bd
$b0$f1░░░░░░░█▄██▀▄░░░░░▄███▄▄░░░░░░███████░░░$fd$bd
$b0$f1░░░░░░▄▀▀▀██▀░░░░░▄▄▄░░▀█░░░░█████████░░$fd$bd
$b0$f1░░░░░▄▀░░░░▄▀░▄░░█▄██▀▄░░░░░██████████░░$fd$bd
$b0$f1░░░░░█░░░░▀░░░█░░░▀▀▀▀▀░░░░░██████████▄░$fd$bd
$b0$f1░░░░░░░▄█▄░░░░░▄░░░░░░░░░░░░██████████▀░$fd$bd
$b0$f1░░░░░░█▀░░░░▀▀░░░░░░░░░░░░░███▀███████░░$fd$bd
$b0$f1░░░▄▄░▀░▄░░░░░░░░░░░░░░░░░░▀░░░██████░░░$fd$bd
$b0$f1██████░░█▄█▀░▄░░██░░░░░░░░░░░█▄█████▀░░░$fd$bd
$b0$f1██████░░░▀████▀░▀░░░░░░░░░░░▄▀█████████▄$fd$bd
$b0$f1██████░░░░░░░░░░░░░░░░░░░░▀▄████████████$fd$bd
$b0$f7██████░░▄░░░░░░░░░░░░░▄░░░██████████████$fd$bd
$b0$f7██████░░░░░░░░░░░░░▄█▀░░▄███████████████$fd$bd
$b0$f7███████▄▄░░░░░░░░░▀░░░▄▀▄███████████████$fd$bd"""

testme2 =\
"""
$b0$f7⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠛⠛⠛⠿⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿$fd$bd
$b0$f3⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⡀⠠⠤⠒⢂⣉⣉⣉⣑⣒⣒⠒⠒⠒⠒⠒⠒⠒⠀⠀⠐⠒⠚⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿$fd$bd
$b0$f1⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⡠⠔⠉⣀⠔⠒⠉⣀⣀⠀⠀⠀⣀⡀⠈⠉⠑⠒⠒⠒⠒⠒⠈⠉⠉⠉⠁⠂⠀⠈⠙⢿⣿⣿⣿⣿⣿$fd$bd
$b0$f1⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠔⠁⠠⠖⠡⠔⠊⠀⠀⠀⠀⠀⠀⠀⠐⡄⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠉⠲⢄⠀⠀⠀⠈⣿⣿⣿⣿⣿$fd$bd
$b0$f1⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠊⠀⢀⣀⣤⣤⣤⣤⣀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠜⠀⠀⠀⠀⣀⡀⠀⠈⠃⠀⠀⠀⠸⣿⣿⣿⣿$fd$bd
$b0$f1⣿⣿⣿⣿⡿⠥⠐⠂⠀⠀⠀⠀⡄⠀⠰⢺⣿⣿⣿⣿⣿⣟⠀⠈⠐⢤⠀⠀⠀⠀⠀⠀⢀⣠⣶⣾⣯⠀⠀⠉⠂⠀⠠⠤⢄⣀⠙⢿⣿⣿$fd$bd
$b0$f1⣿⡿⠋⠡⠐⠈⣉⠭⠤⠤⢄⡀⠈⠀⠈⠁⠉⠁⡠⠀⠀⠀⠉⠐⠠⠔⠀⠀⠀⠀⠀⠲⣿⠿⠛⠛⠓⠒⠂⠀⠀⠀⠀⠀⠀⠠⡉⢢⠙⣿$fd$bd
$b0$f1⣿⠀⢀⠁⠀⠊⠀⠀⠀⠀⠀⠈⠁⠒⠂⠀⠒⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⢀⣀⡠⠔⠒⠒⠂⠀⠈⠀⡇⣿$fd$bd
$b0$f1⣿⠀⢸⠀⠀⠀⢀⣀⡠⠋⠓⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠈⠢⠤⡀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⡠⠀⡇⣿$fd$bd
$b0$f1⣿⡀⠘⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠈⠑⡦⢄⣀⠀⠀⠐⠒⠁⢸⠀⠀⠠⠒⠄⠀⠀⠀⠀⠀⢀⠇⠀⣀⡀⠀⠀⢀⢾⡆⠀⠈⡀⠎⣸⣿$fd$bd
$b0$f1⣿⣿⣄⡈⠢⠀⠀⠀⠀⠘⣶⣄⡀⠀⠀⡇⠀⠀⠈⠉⠒⠢⡤⣀⡀⠀⠀⠀⠀⠀⠐⠦⠤⠒⠁⠀⠀⠀⠀⣀⢴⠁⠀⢷⠀⠀⠀⢰⣿⣿$fd$bd
$b0$f1⣿⣿⣿⣿⣇⠂⠀⠀⠀⠀⠈⢂⠀⠈⠹⡧⣀⠀⠀⠀⠀⠀⡇⠀⠀⠉⠉⠉⢱⠒⠒⠒⠒⢖⠒⠒⠂⠙⠏⠀⠘⡀⠀⢸⠀⠀⠀⣿⣿⣿$fd$bd
$b0$f1⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠑⠄⠰⠀⠀⠁⠐⠲⣤⣴⣄⡀⠀⠀⠀⠀⢸⠀⠀⠀⠀⢸⠀⠀⠀⠀⢠⠀⣠⣷⣶⣿⠀⠀⢰⣿⣿⣿$fd$bd
$b0$f1⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠁⢀⠀⠀⠀⠀⠀⡙⠋⠙⠓⠲⢤⣤⣷⣤⣤⣤⣤⣾⣦⣤⣤⣶⣿⣿⣿⣿⡟⢹⠀⠀⢸⣿⣿⣿$fd$bd
$b0$f1⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠑⠀⢄⠀⡰⠁⠀⠀⠀⠀⠀⠈⠉⠁⠈⠉⠻⠋⠉⠛⢛⠉⠉⢹⠁⢀⢇⠎⠀⠀⢸⣿⣿⣿$fd$bd
$b0$f7⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠈⠢⢄⡉⠂⠄⡀⠀⠈⠒⠢⠄⠀⢀⣀⣀⣰⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⢀⣎⠀⠼⠊⠀⠀⠀⠘⣿⣿⣿$fd$bd
$b0$f7⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠉⠢⢄⡈⠑⠢⢄⡀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⢀⠀⠀⠀⠀⠀⢻⣿⣿$fd$bd
$b0$f7⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⡈⠑⠢⢄⡀⠈⠑⠒⠤⠄⣀⣀⠀⠉⠉⠉⠉⠀⠀⠀⣀⡀⠤⠂⠁⠀⢀⠆⠀⠀⢸⣿⣿$fd$bd
$b0$f7⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠁⠉⠒⠂⠤⠤⣀⣀⣉⡉⠉⠉⠉⠉⢀⣀⣀⡠⠤⠒⠈⠀⠀⠀⠀⣸⣿⣿$fd$bd
$b0$f7⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿$fd$bd
$b0$f7⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣤⣤⣤⣤⣀⣀⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿$fd$bd"""

# import esper
@dataclass
class _placeholder:
    renderables = [Renderable(testme2),Renderable(testme2)]
    def get_component(self,*a):
        return [
            Region('NULL',2,-1,(0,0),0),
            Region('a',23,-1,(0,0),0),
            Region('b',21,-1,(25,0),0),
            # Region('b',23,-1,(22,0),1),
        ]
    def component_for_entity(self,index,*a):
        return self.renderables[index]

from formatter import transform

esper = _placeholder()

def renderRegions(screen,debug=True): #a curses.window object


    for region in esper.get_component(Region):
        renderable = esper.component_for_entity(region.renderable, Renderable)

        height = region.height if region.height > 0 else curses.LINES  #max out the sizes
        width  = region.width  if region.width  > 0 else curses.COLS   #

        if (height + region.corner[0]) > curses.LINES:
            height -= abs(curses.LINES - (height + region.corner[0]))  # adjust right overflows

        if (width  + region.corner[1]) > curses.COLS:
            width  -= abs(curses.COLS  - (width  + region.corner[1]))  #


        fixed = transform(curses, renderable.visual)
        prev_max = 0

        top  = region.corner[0]+1
        left = region.corner[1]+1
        # DEBUG(f"Drawing from {top},{left}")
        for text, color in fixed:
            if text == '\n':
                top += 1
                screen.addstr(top,left,text,color)
                prev_max = 0
            else:
                screen.addstr(top,left+prev_max,text,color)
                prev_max += len(text)

        screen.refresh()


def _render(screen,debug=False):
    curses.use_default_colors()
    screen.erase()
    renderRegions(screen,debug)
    screen.refresh()
    if debug: screen.getch()


def render(screen):
    _render(screen,True)

if __name__ == '__main__':
    curses.wrapper(render)
