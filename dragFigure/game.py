from os import read
import pygame
import time
import random
from image import load
from settings import *
from background import Background
from hand import Hand
from hand_tracking import HandTracking
from figure import Figure
from bomb import Bomb
from bag import Bag
import cv2
import ui

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.background = Background()

        # Load camera
        self.cap = cv2.VideoCapture(0)

        self.sounds = {}
        self.sounds["explosion"] = pygame.mixer.Sound(f"Assets/Sounds/explosion.wav")
        self.sounds["explosion"].set_volume(SOUNDS_VOLUME)
        self.sounds["screaming"] = pygame.mixer.Sound(f"Assets/Sounds/screaming.wav")
        self.sounds["screaming"].set_volume(SOUNDS_VOLUME)  


    def reset(self): # reset all the needed variables
        self.bags = []
        self.hand_tracking = HandTracking()
        self.hand = Hand()
        self.figuresQuantity = 0
        self.bombsQuantity = 0
        self.objects = []
        self.objects_spawn_timer = 0
        self.score = 0
        self.highscore = int(self.loadScore("C:\\tmp\\score.txt"))
        self.game_start_time = time.time()


    def spawn_objects(self):
        t = time.time()
        if t > self.objects_spawn_timer:
            self.objects_spawn_timer = t + FIGURES_SPAWN_TIME

            # increase the probability that the object will be a bomb over time
            nb = (GAME_DURATION-self.time_left)/GAME_DURATION * 100  / 2  # increase from 0 to 50 during all  the game (linear)
            if random.randint(0, 100) < nb:
                self.objects.append(Bomb())
                self.bombsQuantity += 1
            else:
                self.objects.append(Figure())
                self.figuresQuantity += 1

            # spawn a other figure after the half of the game
            if self.time_left < GAME_DURATION/2:
                self.objects.append(Figure())

    def spawn_bags(self):
        for x in range(1, 7):
            self.bags.append(Bag(x))

    def load_camera(self):
        _, self.frame = self.cap.read()


    def set_hand_position(self):
        self.frame = self.hand_tracking.scan_hands(self.frame)
        (x, y) = self.hand_tracking.get_hand_center()
        self.hand.rect.center = (x, y)

    def draw(self):
        # draw the background
        self.background.draw(self.surface)
        # draw the objects
        for object in self.objects:
            object.draw(self.surface)
            #object.draw_hitbox(self.surface)
        # draw the hand
        self.hand.draw(self.surface)
        #self.hand.draw_hitbox(self.surface)
        # draw the bags
        for bag in self.bags:
            bag.draw(self.surface)
            #bag.draw_hitbox(self.surface)
        # draw the score
        ui.draw_text(self.surface, f"Score : {self.score}", (5, 5), COLORS["score"], font=FONTS["medium"],
                    shadow=True, shadow_color=(0,0,0))
        # draw the highscore
        ui.draw_text(self.surface, f"HighScore : {self.highscore}", (5, 50), COLORS["highscore"], font=FONTS["medium"],
                    shadow=True, shadow_color=(0,0,0))
        # draw the time left
        timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
        ui.draw_text(self.surface, f"Time left : {self.time_left}", (SCREEN_WIDTH//1.45, 5),  timer_text_color, font=FONTS["medium"],
                    shadow=True, shadow_color=(0,0,0))


    def game_time_update(self):
        self.time_left = max(round(GAME_DURATION - (time.time() - self.game_start_time), 1), 0)

    def saveScore(self, fpath, data_in):
        with open(fpath, "w") as file_in:
            file_in.write(data_in)

    def loadScore(self, fpath):
        try:
            file = open(fpath, "r")
            data = file.read()
        except IOError:
            print("File not found or path is incorrect")
            data = 0
        finally:
            return data

    def update(self):

        self.load_camera()
        self.set_hand_position()
        self.game_time_update()
        #print(self.highscore)

        self.draw()

        if self.time_left > 0:
            self.spawn_objects()
            if self.bags==[]:
                self.spawn_bags()
            (x, y) = self.hand_tracking.get_hand_center()
            self.hand.rect.center = (x, y)
            self.hand.left_click = self.hand_tracking.hand_closed
            #print("Hand closed", self.hand.left_click)
            if self.hand.left_click:
                self.hand.image = self.hand.image_smaller.copy()
            else:
                self.hand.image = self.hand.orig_image.copy()
            self.score = self.hand.kill_objects(self.objects, self.score, self.sounds)
            for object in self.objects:
                object.move()
            for bag in self.bags:
               self.score = bag.kill_figures(self.objects, self.score, self.sounds)

        else: # when the game is over
            # Save Game Data
            if self.score > self.highscore:
                self.saveScore("C:\\tmp\\score.txt", str(self.score))
            if ui.button(self.surface, 540, "Continue", click_sound=self.sounds["explosion"]):
                return "menu"


        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)
