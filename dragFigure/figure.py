import pygame
import random
import time

from pygame import mouse
import image
from settings import *

class Figure:
    def __init__(self):
        self.type = "figure"
        #size
        random_size_value = random.uniform(FIGURE_SIZE_RANDOMIZE[0], FIGURE_SIZE_RANDOMIZE[1])
        size = (int(FIGURES_SIZES[0] * random_size_value), int(FIGURES_SIZES[1] * random_size_value))
        # moving
        moving_direction, start_pos = self.define_spawn_pos(size)
        # sprite
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0]//1.4, size[1]//1.4)
        self.frame = random.randint(1,6)
        self.images = [image.load(f"Assets/figures/{self.frame}.png", size=size, flip=moving_direction=="right")] # load the images
        self.current_frame = 0
        self.animation_timer = 0


    def define_spawn_pos(self, size): # define the start pos and moving vel of the figure
        vel = random.uniform(FIGURES_MOVE_SPEED["min"], FIGURES_MOVE_SPEED["max"])
        moving_direction = random.choice(("left", "right"))
        #moving_direction = random.choice(("left", "right", "up", "down"))
        if moving_direction == "right":
            start_pos = (-size[0], random.randint(size[1], SCREEN_HEIGHT-(size[1]*5)))
            self.vel = [vel, 0]
        if moving_direction == "left":
            start_pos = (SCREEN_WIDTH + size[0], random.randint(size[1], SCREEN_HEIGHT-(size[1]*5)))
            self.vel = [-vel, 0]
        # if moving_direction == "up":
        #     start_pos = (random.randint(size[0], SCREEN_WIDTH-size[0]), SCREEN_HEIGHT+size[1])
        #     self.vel = [0, -vel]
        # if moving_direction == "down":
        #     start_pos = (random.randint(size[0], int(SCREEN_WIDTH/2)-size[0]), -size[1])
        #     print(start_pos)
        #     self.vel = [0, vel]
        return moving_direction, start_pos


    def move(self):
        self.rect.move_ip(self.vel)
            


    def animate(self): # change the frame of the object when needed
        t = time.time()
        if t > self.animation_timer:
            self.animation_timer = t + ANIMATION_SPEED
            self.current_frame += 1
            if self.current_frame > len(self.images)-1:
                self.current_frame = 0


    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (200, 60, 0), self.rect)



    def draw(self, surface):
        self.animate()
        image.draw(surface, self.images[self.current_frame], self.rect.center, pos_mode="center")
        if DRAW_HITBOX:
            self.draw_hitbox(surface)

    def drag(self, handPos, dragged=False):
        if dragged:
            self.rect.x = handPos[0] - self.rect.width/2
            self.rect.y = handPos[1] - self.rect.height/2

    def kill(self, figures): # remove the figure from the list and return points given
        figures.remove(self)
        return 1
