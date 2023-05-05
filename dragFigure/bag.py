import pygame
import random
import time

from pygame import mouse
import image
from settings import *

class Bag:
    def __init__(self, id):
        #size
        size = (int(BAG_SIZES[0]*3), int(BAG_SIZES[1]*3))
        # sprite
        self.rect = pygame.Rect(int((SCREEN_HEIGHT/3.5*id)-(size[0])), SCREEN_HEIGHT-(size[1]), size[0]//1.4, size[1]//1.4)
        self.frame = id
        self.images = [image.load(f"Assets/bags/{self.frame}.png", size=size)] # load the images
        self.current_frame = 0
        self.animation_timer = 0

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (200, 60, 0), self.rect)

    def draw(self, surface):
        image.draw(surface, self.images[self.current_frame], self.rect.center, pos_mode="center")
        if DRAW_HITBOX:
            self.draw_hitbox(surface)

    def on_object(self, objects): # return a list with all objects that collide with the hitbox
        return [object for object in objects if self.rect.colliderect(object.rect)]

    def kill_figures(self, objects, score, sounds):
        for object in self.on_object(objects):
            print(object)
            if object.frame == self.frame:  # if drop in the right bag
                object_score = object.kill(objects)
                score += object_score
                sounds["explosion"].play()
            else:
                object_score = object.kill(objects)
                sounds["explosion"].play()
        return score