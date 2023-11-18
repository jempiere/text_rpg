import esper
from dataclasses import dataclass
import curses
import threading
import rich
from rich import print
import io
import sys



@dataclass
class Renderable:
    visual: str


@dataclass
class Region:
    identifier: str
    height: int
    width: int
    corner: tuple
    layer: int
    renderable: int

magenta = ''#'\x1B[0;31m'
clear   = ''#'\x1B[0m'
uline   = ''#'\x1B[0;31m'
bold    = ''#'\x1B[0;31m'


# proxy = esper
@dataclass
class P:
    renderables = [Renderable(f"{magenta}ligma{clear}"), Renderable(f"{uline}underlined broseph{clear}"), Renderable(f"{bold}poggers{clear}")]
    def get_component(self,*a):
        return [Region('NULL',8,-1,(10,0),-1,-1),Region('a',5,-1,(0,0),-1,0), Region('b',5,-1,(5,8),-1,1), Region('c',8,-1,(10,0),-1,2)]
    def component_for_entity(self,index, *a):
        return self.renderables[index]
proxy = P()
"""
proxy can be set equal to esper
for the proper implementation
"""

@dataclass
class Renderable:
    visual: str


@dataclass
class Region:
    identifier: str
    height: int
    width: int
    corner: tuple
    layer: int
    renderable: int


def pprint(*a,**kw) -> None:
    output = io.StringIO()
    print(*a,**kw,file=output)
    contents = output.getvalue()
    output.close()
    return contents


def render(screen):
    for region in proxy.get_component(Region):
        renderable = proxy.component_for_entity(region.renderable,Renderable)
        height = curses.LINES
        width  = curses.COLS

        if region.height > 0: height = region.height
        if region.width  > 0: width  = region.width

        if height+region.corner[0] > curses.LINES:
            height -= abs(curses.LINES - (height+region.corner[0]))

        if width+region.corner[1] > curses.COLS:
            width -= abs(curses.COLS - (width+region.corner[1]))
          

        window = curses.newwin(height,width,region.corner[0],region.corner[1])
        window.box()
        window.addstr(0,1,f"{region.identifier} {region.renderable}")
        window.addstr(2,4,f"{renderable.visual}")
        window.refresh()
        screen.refresh()

    # screen.refresh()
        


# # def render(screen):
#     for region in proxy.get_component(Region):
#         height = region.height if region.height >= 0 else curses.LINES
#         width  = region.width  if region.width  >= 0 else curses.COLS

#         # window# = curses.newwin(height, width, region.corner[0], region.corner[1])
#         screen.box()

#         screen.addstr(5,5,f"{height},{width},{region.corner}")
#         screen.addstr(1,1,region.identifier)

#         renderable = proxy.component_for_entity(region.renderable, Renderable)
#         screen.addstr(height+region.corner[0], width+region.corner[1],f"{renderable.visual}",curses.color_pair(1))
#         screen.refresh()


def main(screen):
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_RED,-1)
    
    screen.erase()
    render(screen)
    screen.refresh()
    screen.getch()


curses.wrapper(main)
