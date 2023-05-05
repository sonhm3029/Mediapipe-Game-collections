import pygame

WINDOW_NAME = "DragFigure Game"
GAME_TITLE = WINDOW_NAME

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700

FPS = 90
DRAW_FPS = True

# sizes
BUTTONS_SIZES = (240, 90)
HAND_SIZE = 200
HAND_HITBOX_SIZE = (60, 80)
FIGURES_SIZES = (50, 40)
FIGURE_SIZE_RANDOMIZE = (1,2) # for each new figure, it will multiply the size with an random value between X and Y
BOMB_SIZES = (50, 50)
BOMB_SIZE_RANDOMIZE = (1.2, 1.5)
BAG_SIZES = (50, 50)

# drawing
DRAW_HITBOX = False # will draw all the hitbox

# animation
ANIMATION_SPEED = 0.08 # the frame of the objects will change every X sec

# difficulty
GAME_DURATION = 60 # the game will last X sec
FIGURES_SPAWN_TIME = 1
FIGURES_MOVE_SPEED = {"min": 1, "max": 5}
BOMB_PENALITY = 1 # will remove X of the score of the player (if he grabs a bomb)

# colors
COLORS = {"title": (255, 210, 40), "score": (120, 90, 255), "highscore": (80, 255, 65), "timer": (255, 255, 255),
            "buttons": {"default": (255, 210, 40), "second":  (255, 185, 0),
                        "text": (255, 255, 255), "shadow": (255, 170, 0)}} # second is the color when the mouse is on the button

# sounds / music
MUSIC_VOLUME = 0.16 # value between 0 and 1
SOUNDS_VOLUME = 1

# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font(None, 40)
FONTS["medium"] = pygame.font.Font(None, 72)
FONTS["big"] = pygame.font.Font(None, 120)
