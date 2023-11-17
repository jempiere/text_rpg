from eloy import *


def yourFunction():
    print("Hello World")


set_handler(Stage.preRender, yourFunction)
