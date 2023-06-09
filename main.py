import pygame as pg
from pygame import Vector2 as V
import sys
from colors import *
from point import Point

pg.init()
pg.font.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

POINT_EVERY = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_colorkey(BLACK)

FPS = 60
clock = pg.time.Clock()

fontSize = 500
myFont = pg.font.Font(None, fontSize)

def draw_points(outlines):
    for points in outlines:
            for p in points:
                pg.draw.circle(screen, GREEN, p, 5)

def main():
    mask_mode = 0

    # Make the text and the text surface
    text = "ABCDE"
    surface_text = myFont.render(text, True, WHITE)
    
    # surface_text = pg.image.load("Image/Cs_logo.png").convert_alpha()
    
    # Gets the edges of the characters
    surface_text = pg.transform.laplacian(surface_text)

    # Finding the text position
    text_pos = V(SCREEN_WIDTH/2 - surface_text.get_width()/2, SCREEN_HEIGHT/2 - surface_text.get_height()/2)

    # Make a mask out of the text surface
    mask = pg.mask.from_surface(surface_text)

    # Finds all of the components from the surface
    masks = mask.connected_components()

    # Connecting the outline positions with the actual text positions
    outlines = [[(p[0] + text_pos.x, p[1] + text_pos.y) for p in points.outline(every=POINT_EVERY)] for points in masks]
    
    point_list = list()
    for points in outlines:
        for p in points:
            point_list.append(Point(p, 5))

    while True:
        
        mx, my = pg.mouse.get_pos()

        clock.tick(FPS)
        screen.fill(GRAY)

        for point in point_list:
            point.draw(screen)
            point.seek_home()
            point.flee(V(mx, my))
            point.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_m:
                    mask_mode = not mask_mode
        pg.display.flip()

if __name__ == "__main__":
    main()