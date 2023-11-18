import esper
from dataclasses import dataclass
import curses
import threading
import rich
from rich import print
import io
import sys
from parsecolors import test_str

DATALOG = []

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
    renderables = [Renderable(f"ligma"), Renderable(f"underlined broseph"), Renderable(f"poggers")]
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

    
    c_line = 3

    flat = []
    for msg, color in test_str(): # a list of lines inside
        sublines = ['']
        for c in msg:
            if c != '\n':
                sublines[-1] += c
                continue
            else:
                sublines.append(c)
        if sublines[0] == '':
            sublines.pop(0)

        for line in sublines:
            flat.append([line,color])
    
    for f in flat:
        DATALOG.append(f)

    # for pair in test_str():
    #     colors = pair[1]
    #     string = pair[0] #.split('\n')  #.split('\n')

    #     lines = ['']
    #     left_offset = 4
    #     for char in string:
    #         if char != '\n':
    #             lines[-1] += char
    #             continue
    #         else:
    #             lines.append(char)
    #     if lines[0] == '':
    #         lines.pop(0)
    prev = c_line
    prevlen = 0
    for f in flat:
        line, colors = f
        DATALOG.append(colors)
        if line == '\n':
            c_line += 1
            prev = c_line - 1

        if line == '\n': screen.addstr(c_line,4,line,colors)
        else: screen.addstr(c_line,4+prevlen,line,colors)

        # if line == '\n':
            # screen.addstr(c_line,4,line,curses.color_pair(colors))
        # else:
            # screen.addstr(c_line,4+prevlen,line,curses.color_pair(colors))


    screen.refresh()
    screen.getch()
    
    screen.erase()
    render(screen)
    screen.refresh()
    screen.getch()


curses.wrapper(main)

for item in DATALOG:
    print(item)
