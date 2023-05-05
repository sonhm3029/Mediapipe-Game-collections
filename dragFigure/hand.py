import pygame
import image
from settings import *
from hand_tracking import HandTracking
import cv2

class Hand:
    def __init__(self):
        self.orig_image = image.load("Assets/hand.png", size=(HAND_SIZE, HAND_SIZE))
        self.image = self.orig_image.copy()
        self.image_smaller = image.load("Assets/hand.png", size=(HAND_SIZE - 50, HAND_SIZE - 50))
        self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, HAND_HITBOX_SIZE[0], HAND_HITBOX_SIZE[1])
        self.left_click = False
        self.dragging = False
        #self.hand_tracking = HandTracking()

    def follow_mouse(self): # change the hand pos center at the mouse pos
        self.rect.center = pygame.mouse.get_pos()
        #self.hand_tracking.display_hand()

    def follow_mediapipe_hand(self, x, y):
        self.rect.center = (x, y)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (200, 60, 0), self.rect)


    def draw(self, surface):
        image.draw(surface, self.image, self.rect.center, pos_mode="center")

        if DRAW_HITBOX:
            self.draw_hitbox(surface)

    def on_object(self, objects): # return a list with all objects that collide with the hand hitbox
        list = [object for object in objects if self.rect.colliderect(object.rect)]
        if list != []:
            return list[0]



    def kill_objects(self, objects, score, sounds): # will kill the objects that collide with the hand when the left mouse button is pressed
        if not self.dragging:
            self.object = self.on_object(objects)
        else:
            self.object = self.object

        if self.left_click and self.object!=None: # if left click
                if self.object.type == "bomb":
                    object_score = self.object.kill(objects)
                    score += object_score
                    sounds["explosion"].play()
                elif self.object.type == "figure":
                    self.dragging = True
                    self.object.drag(self.rect.center, True)
                    self.object = self.object
        else:
            if self.dragging:
                self.object.drag(self.rect.center, False)
            self.left_click = False
            self.dragging = False
        return score
