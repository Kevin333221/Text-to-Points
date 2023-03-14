import pygame as pg
from pygame import Vector2 as V
from colors import *
from random import randint as r

def map(value, left_min, left_max, right_min, right_max):
    return right_min + ((right_max - right_min) / (left_max - left_min)) * (value - left_min)

class Point:
    def __init__(self, pos: tuple, radius: int):
        self.pos = V((r(0, 1200), r(0, 600)))
        self.vel = V()
        self.acc = V()
        self.r = radius

        self.home = V(pos)
        self.max_speed = 3
        self.max_force = 0.3

    def draw(self, screen: pg.surface.Surface):
        pg.draw.circle(screen, WHITE, self.pos, self.r)

    def add_force(self, force: tuple):
        self.acc += V(force) * self.max_force

    def seek_home(self):
        home_vector = V()
        home_vector = self.home - self.pos
        distance = home_vector.magnitude()
        newMag = self.max_speed
        if distance < 1000:
            newMag = map(distance, 0, 1000, 0, self.max_speed)

        if home_vector.magnitude() != 0:
            # Normalizing the vector and sets its magnitude to max_speed and 
            # constrains the effect to max_force
            home_vector = home_vector.normalize()
            home_vector *= newMag
            home_vector = home_vector.clamp_magnitude(self.max_force)

            # Adds the force to the acceleration
            self.add_force(home_vector)

    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0