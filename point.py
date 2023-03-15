import pygame as pg
from pygame import Vector2 as V
from colors import *
from random import randint as r
from math import floor

def map(value, left_min, left_max, right_min, right_max):
    return right_min + ((right_max - right_min) / (left_max - left_min)) * (value - left_min)

class Point:
    def __init__(self, pos: tuple, radius: int):
        self.pos = V((r(0, 1200), r(0, 600)))
        self.vel = V()
        self.acc = V()
        self.r = radius

        self.home = V(pos)
        self.max_speed = 10
        self.max_force = 0.8

    def draw(self, screen: pg.surface.Surface):
        if self.pos.distance_to(self.home) < 20:
            pg.draw.circle(screen, WHITE, self.pos, self.r)
        else:
            pg.draw.circle(screen, RED, self.pos, self.r)

    def add_force(self, force: tuple, weight):
        self.acc += V(force) * self.max_force * weight

    def seek_home(self):
        steer = V()
        home_vector = V()
        home_vector = self.home - self.pos
        distance = home_vector.magnitude()
        newMag = self.max_speed
        
        if distance < 100:
            newMag = map(distance, 0, 100, 0, self.max_speed)
            
        if floor(home_vector.magnitude()) != 0 and floor(home_vector.length()) != 0:
            home_vector.scale_to_length(newMag)
            # Normalizing the vector and sets its magnitude to max_speed and 
            # constrains the effect to max_force
            steer = home_vector - self.vel
            if steer.length() != 0:
                steer = steer.clamp_magnitude(self.max_force)
            
        # Adds the force to the acceleration
        self.add_force(steer, 1)
        
    def flee(self, target: V):
        steer = V()
        home_vector = V()
        home_vector = target - self.pos
        distance = home_vector.magnitude()
        newMag = self.max_speed
        
        if distance < 100:
            if floor(home_vector.magnitude()) != 0 and floor(home_vector.length()) != 0:
                home_vector.scale_to_length(newMag)
                home_vector *= -1
                # Normalizing the vector and sets its magnitude to max_speed and 
                # constrains the effect to max_force
                steer = home_vector - self.vel
                if steer.length() != 0:
                    steer = steer.clamp_magnitude(self.max_force)
            
        # Adds the force to the acceleration
        self.add_force(steer, 5)

    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0