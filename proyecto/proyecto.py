import sys
import random
from gl import Render
from obj import Texture
r = Render(1000,600)
def mario():
    """
    Draws a cube at an angle so it is more interesting
    """
    t = Texture("./marioD.bmp")
    r.load("./mario_obj.obj", (100, 2, 1), (3.5, 3.5, 3.5), texture=t)

mario()
print('mario done')
def luigi():
    """
    Draws a cube at an angle so it is more interesting
    """
    t = Texture("./luigiD.bmp")
    r.load("./Luigi_obj.obj", (110, 2, 1), (3.5, 3.5, 3.5), texture=t)

def goomba():
    """
    Draws a cube at an angle so it is more interesting
    """
    t = Texture("./goomba_grp.bmp")
    r.load("./goomba.obj", (110, 2, 1), (3.5, 3.5, 3.5), texture=t)


luigi()
print('luigi done')

goomba()
print('goomba done')
r.display('out.bmp')
