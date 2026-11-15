from pathlib import Path
import os
import sys
import pygame
from pgzero import game as pgz_game, loaders
import random
import pyaudio
import numpy as np

os.chdir(Path(__file__).resolve().parent.parent)

from pgzero.builtins import keyboard

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from modules.pgzhelper import Actor
else:
    from .pgzhelper import Actor

from setting import (
    FPS,
    SCREEN_H,
    SCREEN_W,
    PATH_STAGE_BLUE_BG,
    PATH_BLUE_BAD,
    PATH_BLUE_POINTING,
    PATH_BLUE_FIST,
    PATH_BLUE_ILOVEU,
    PATH_BLUE_VICTORY,
    PATH_BLUE_OPENHAND,
    PATH_STAGE_BLUE_GREY_STAR,
    # you can add blue bg music path here later in setting.py
)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Blue Stage")
    clock = pygame.time.Clock()

asset_root = Path(__file__).resolve().parent.parent / "assets"
loaders.set_root(str(asset_root))

# asset variables
img_blue_bg = None
img_blue_bad = None
img_blue_pointing = None
img_blue_fist = None
img_blue_iloveu = None
img_blue_victory = None
img_blue_openhand = None
img_blue_grey_star = None

runner = None


def stage_blue_enter():
    # prepare mic / audio resource if you need later
    pass


def stage_blue_exit():
    # clean up mic / audio resource if you need later
    pass


def load_assets():
    global img_blue_bg, img_blue_bad, img_blue_pointing, img_blue_fist, img_blue_iloveu
    global img_blue_victory, img_blue_openhand, img_blue_grey_star, timer_font

    if img_blue_bad is not None:
        return

    img_blue_bg = pygame.image.load(PATH_STAGE_BLUE_BG).convert_alpha()
    img_blue_bad = pygame.image.load(PATH_BLUE_BAD).convert_alpha()
    img_blue_pointing = pygame.image.load(PATH_BLUE_POINTING).convert_alpha()
    img_blue_fist = pygame.image.load(PATH_BLUE_FIST).convert_alpha()
    img_blue_iloveu = pygame.image.load(PATH_BLUE_ILOVEU).convert_alpha()
    img_blue_victory = pygame.image.load(PATH_BLUE_VICTORY).convert_alpha()
    img_blue_openhand = pygame.image.load(PATH_BLUE_OPENHAND).convert_alpha()
    img_blue_grey_star = pygame.image.load(PATH_STAGE_BLUE_GREY_STAR).convert_alpha()

    timer_font = pygame.font.Font(None, 36)


def stage_blue_start():
    load_assets()
    stage_blue_enter()


def stage_blue_update(dt):
    # BLANK, you fill logic later
    load_assets()
    pass


def stage_blue_draw(screen):
    load_assets()
    pgz_game.screen = screen
    screen.blit(img_blue_bg, (0, 0))


if __name__ == "__main__":
    running = True
    stage_blue_start()
    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keyboard._press(event.key)
            elif event.type == pygame.KEYUP:
                keyboard._release(event.key)
        stage_blue_update(dt)
        stage_blue_draw(screen)
        pygame.display.flip()
    pygame.quit()
