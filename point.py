import pygame as pg
from pygame import Vector2 as V
from colors import *

class Point:
    def __init__(self, pos: tuple, radius: int):
        self.pos = V(pos)
        self.vel = V()
        self.acc = V()
        self.r = radius

    def draw(self, screen: pg.surface.Surface):
        pg.draw.circle(screen, WHITE, self.pos, self.r)

    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0