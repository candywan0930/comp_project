import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import cv2
import pygame
import numpy as np
import pgzrun


from setting import (
    FPS, 
    PATH_HAIRDRY_R, 
    PATH_HOME_BG, 
    PATH_HOME_BG_MUSIC, 
    PATH_LAMP_B, 
    PATH_MIRROR_BG, 
    PATH_PLANT_G, 
    PATH_POINTER, 
    PATH_WASH, 
    SCREEN_H, 
    SCREEN_W, 
    STATE_BLUE, 
    STATE_GREEN, 
    STATE_HOME, 
    STATE_RED)

WIDTH = SCREEN_W
HEIGHT = SCREEN_H
TITLE = "Heart of Emotion"

from modules.stage_red import stage_red_draw, stage_red_start, stage_red_update
from modules.stage_blue import stage_blue_draw, stage_blue_start, stage_blue_update

pointer_offset_x = 45
pointer_offset_y = 45

assets_loaded = False
img_mirror_bg = None
img_lamp_b = None
img_home_bg = None
img_hairdry_r = None
img_plant_g = None
img_wash = None
img_pointer = None
rect_hairdry_r = None
rect_plant_g = None
rect_lamp_b = None
center_hairdry_r = None
center_plant_g = None
center_lamp_b = None
hover_scale = 1.05
hover_btn = None

current_stage= STATE_HOME
mouse_pos = (0, 0)


def load_assets():
    global assets_loaded
    global img_mirror_bg, img_lamp_b, img_home_bg, img_hairdry_r
    global img_plant_g, img_wash, img_pointer
    global rect_hairdry_r, rect_plant_g, rect_lamp_b
    global center_hairdry_r, center_plant_g, center_lamp_b

    if assets_loaded:
        return

    pygame.mixer.init()
    img_mirror_bg = pygame.image.load(PATH_MIRROR_BG).convert_alpha()
    img_lamp_b = pygame.image.load(PATH_LAMP_B).convert_alpha()
    img_home_bg = pygame.image.load(PATH_HOME_BG).convert_alpha()
    img_hairdry_r = pygame.image.load(PATH_HAIRDRY_R).convert_alpha()
    img_plant_g = pygame.image.load(PATH_PLANT_G).convert_alpha()
    img_wash = pygame.image.load(PATH_WASH).convert_alpha()
    img_pointer = pygame.image.load(PATH_POINTER).convert_alpha()
    img_pointer = pygame.transform.scale(img_pointer, (100, 100))

    pygame.mixer.music.load(PATH_HOME_BG_MUSIC)

    rect_hairdry_r = pygame.Rect(0, 210, img_hairdry_r.get_width(), img_hairdry_r.get_height())
    rect_plant_g = pygame.Rect(910, 175, img_plant_g.get_width(), img_plant_g.get_height())
    rect_lamp_b = pygame.Rect(390, 0, img_lamp_b.get_width(), img_lamp_b.get_height())

    center_hairdry_r = (rect_hairdry_r.centerx, rect_hairdry_r.centery)
    center_plant_g = (rect_plant_g.centerx, rect_plant_g.centery)
    center_lamp_b = (rect_lamp_b.centerx, rect_lamp_b.centery)
    assets_loaded = True


def update(dt):
    global current_stage, mouse_pos, hover_btn
    load_assets()
    mouse_pos = pygame.mouse.get_pos()
    #music control
    if current_stage == STATE_HOME:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
    elif current_stage != STATE_RED:
        pygame.mixer.music.stop()
    elif current_stage == STATE_GREEN:
        pygame.mixer.music.stop()

    if current_stage == STATE_HOME:
        hover_btn = None
        if rect_hairdry_r.collidepoint(mouse_pos):
            hover_btn = "hairdry_r"
        elif rect_plant_g.collidepoint(mouse_pos):
            hover_btn = "plant_g"
        elif rect_lamp_b.collidepoint(mouse_pos):
            hover_btn = "lamp_b"
    
        
    elif current_stage == STATE_RED:
        stage_red_update(dt)
    elif current_stage == STATE_GREEN:
        pass
    elif current_stage == STATE_BLUE:
        stage_blue_update(dt)

def draw():
    load_assets()
    screen.fill((0, 0, 0))

    #Home page load png
    if current_stage == STATE_HOME:
        screen.blit(img_mirror_bg, (0, 0))

        #lamp_b animation
        if hover_btn =="lamp_b":
            w=int(img_lamp_b.get_width() * hover_scale)
            h=int(img_lamp_b.get_height() * hover_scale)
            scaled_img_lamp_b = pygame.transform.scale(img_lamp_b, (w, h))
        else:
            scaled_img_lamp_b = img_lamp_b
        r= scaled_img_lamp_b.get_rect(center=center_lamp_b)
        screen.blit(scaled_img_lamp_b, r)

        screen.blit(img_home_bg, (0, 0))

        #hairdry_r animation
        if hover_btn =="hairdry_r":
            w=int(img_hairdry_r.get_width() * hover_scale)
            h=int(img_hairdry_r.get_height() * hover_scale)
            scaled_img_hairdry_r = pygame.transform.scale(img_hairdry_r, (w, h))
        else:
            scaled_img_hairdry_r = img_hairdry_r
        r= scaled_img_hairdry_r.get_rect(center=center_hairdry_r)
        screen.blit(scaled_img_hairdry_r, r)

        #plant_g animation
        if hover_btn =="plant_g":
            w=int(img_plant_g.get_width() * hover_scale)
            h=int(img_plant_g.get_height() * hover_scale)
            scaled_img_plant_g = pygame.transform.scale(img_plant_g, (w, h))
        else:
            scaled_img_plant_g = img_plant_g
        r= scaled_img_plant_g.get_rect(center=center_plant_g)
        screen.blit(scaled_img_plant_g, r)

        screen.blit(img_wash, (0, 0))
        screen.blit(img_pointer, (mouse_pos[0] - pointer_offset_x, mouse_pos[1] - pointer_offset_y))

    elif current_stage == STATE_RED:
        stage_red_draw(screen)
        #modules.stage_red.stage_red_start()


    elif current_stage == STATE_GREEN:
        pass

    elif current_stage == STATE_BLUE:
        stage_blue_draw(screen)

def on_mouse_down(pos, button):
    global current_stage
    load_assets()
    if (
        current_stage == STATE_HOME
        and rect_hairdry_r.collidepoint(pos)
    ):
        stage_red_start()
        current_stage = STATE_RED
    elif current_stage == STATE_HOME and rect_lamp_b.collidepoint(pos):
        stage_blue_start()
        current_stage = STATE_BLUE


pgzrun.go()