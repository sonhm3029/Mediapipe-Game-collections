import sys
import pygame as pg
from pygame.math import Vector2


pg.init()

WHITE = (255, 255, 255)
RED   = (255,   0,   0)

screen = pg.display.set_mode((1024, 768))

selected_rect = None  # Currently selected rectangle.
rectangles = []
for y in range(5):
    rectangles.append(pg.Rect(20, 30*y, 17, 17))
# As a list comprehension.
# rectangles = [pg.Rect(20, 30*y, 17, 17) for y in range(5)]

clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for rectangle in rectangles:
                    if rectangle.collidepoint(event.pos):
                        offset = Vector2(rectangle.topleft) - event.pos
                        selected_rect = rectangle
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                selected_rect = None
        elif event.type == pg.MOUSEMOTION:
            if selected_rect:
                selected_rect.topleft = event.pos + offset

    screen.fill(WHITE)
    for rectangle in rectangles:
        pg.draw.rect(screen, RED, rectangle)

    pg.display.flip()
    clock.tick(30)

pg.quit()
sys.exit()