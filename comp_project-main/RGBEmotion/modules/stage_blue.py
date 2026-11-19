from pathlib import Path
import os
import sys
import pygame
from pgzero import game as pgz_game, loaders
import random
import pyaudio
import numpy as np
import cv2  
import mediapipe as mp

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
    PATH_STAGE_BLUE_LIGHT_STAR,
    PATH_BLUE_GOOD
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
img_blue_good = None
img_blue_light_star = None
blue_stars = []
star_spawn_timer = 0.0
runner = None
blue_gestures = []
current_gesture = None
gesture_sequence = []
show_index = 0
show_timer = 0
cap = None
detected_gesture = None
hands = None
camera_surface = None
is_gesture_matched = False
score = 0
answer_index = 0
wait_timer = 0.0
blue_timer = 60.0
blue_game_over = False
blue_home_btn_rect = pygame.Rect(0, 0, 240, 64)

from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

recognizer = None

def stage_blue_enter():
    global cap, hands, recognizer
    if cap is None:
        cap = cv2.VideoCapture(0)  # 打开摄像头
    if recognizer is None:
        model_path = str(Path(__file__).resolve().parents[2] / "gesture_recognizer.task")
        base_options = mp_python.BaseOptions(model_asset_path=model_path)
        # for easier recognition
        options = mp_vision.GestureRecognizerOptions(
            base_options=base_options,
            min_hand_detection_confidence=0.3,
            min_hand_presence_confidence=0.3,
        )
        recognizer = mp_vision.GestureRecognizer.create_from_options(options)
    

    # prepare mic / audio resource if you need later
    pass


def stage_blue_exit():
    # clean up mic / audio resource if you need later
    pass


def load_assets():
    global img_blue_bg, img_blue_bad, img_blue_pointing, img_blue_fist, img_blue_iloveu
    global img_blue_victory, img_blue_openhand, img_blue_grey_star, timer_font, img_blue_good, img_blue_light_star

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
    img_blue_light_star = pygame.image.load(PATH_STAGE_BLUE_LIGHT_STAR).convert_alpha()
    img_blue_good = pygame.image.load(PATH_BLUE_GOOD).convert_alpha()
    star_scale = 0.5
    img_blue_grey_star = pygame.transform.smoothscale(
        img_blue_grey_star,
        (max(1, int(img_blue_grey_star.get_width() * star_scale)), max(1, int(img_blue_grey_star.get_height() * star_scale))),
    )
    img_blue_light_star = pygame.transform.smoothscale(
        img_blue_light_star,
        (max(1, int(img_blue_light_star.get_width() * star_scale)), max(1, int(img_blue_light_star.get_height() * star_scale))),
    )


    timer_font = pygame.font.Font(None, 36)

blue_bgm_sound = None

blue_bgm_sound = None


def play_blue_bgm():
    global blue_bgm_sound
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if blue_bgm_sound is not None and blue_bgm_sound.get_num_channels() > 0:
            return
        bgm_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "stage_blue_bg.wav")
        )
        if blue_bgm_sound is None:
            blue_bgm_sound = pygame.mixer.Sound(bgm_path)
        blue_bgm_sound.stop()
        blue_bgm_sound.set_volume(0.8)
        blue_bgm_sound.play(-1)
    except Exception as e:
        print("BGM error:", type(e), e)


def stop_blue_bgm():
    global blue_bgm_sound
    try:
        if blue_bgm_sound is not None:
            blue_bgm_sound.stop()
    except Exception as e:
        print("Stop BGM error:", e)

blue_correct_sfx = None

def play_blue_correct_sfx():
    global blue_correct_sfx
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if blue_correct_sfx is None:
            sfx_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "assets", "audio", "stage_blue_correct.wav")
            )
            print("SFX path:", sfx_path, "exists:", os.path.exists(sfx_path))
            blue_correct_sfx = pygame.mixer.Sound(sfx_path)
        blue_correct_sfx.set_volume(0.8)
        ch = blue_correct_sfx.play()
        print("SFX played, channel:", ch)
    except Exception as e:
        print("Correct SFX error:", type(e), e)

def stage_blue_start():
    global blue_gestures, current_gesture, gesture_sequence, show_index, show_timer, answer_index, score, wait_timer, blue_timer, blue_stars, star_spawn_timer, blue_game_over
    wait_timer = 0.0
    blue_game_over = False
    blue_stars = []
    star_spawn_timer = 0.0
    if blue_timer <= 0:
        blue_timer = 60.0
        score = 0


    load_assets()
    stage_blue_enter()
    play_blue_bgm()

    blue_gestures = [
        (img_blue_bad, "Thumb_Down"),
        (img_blue_pointing, "Pointing_Up"),
        (img_blue_fist, "Closed_Fist"),
        (img_blue_iloveu, "ILoveYou"),
        (img_blue_victory, "Victory"),
        (img_blue_openhand, "Open_Palm"),
        (img_blue_good, "Thumb_Up")
    ]
   
    seq_len = min(3 + score, len(blue_gestures))
    gesture_sequence = []
    for _ in range(seq_len):
        choice = random.choice(blue_gestures)
        while len(gesture_sequence) > 0 and choice[1] == gesture_sequence[-1][1]:
            choice = random.choice(blue_gestures)
        gesture_sequence.append(choice)
    current_gesture = gesture_sequence[0]
    show_index = 0
    show_timer = 0
    answer_index = 0
    wait_timer = 0

def next_blue_image():
    global current_gesture
    current_gesture = random.choice(blue_gestures)


def stage_blue_update(dt):
    global detected_gesture, camera_surface, score, current_gesture, show_index, show_timer, answer_index, wait_timer, blue_timer, blue_stars, star_spawn_timer, blue_game_over
    load_assets()

    if blue_game_over:
        return
    blue_timer -= dt
    if blue_timer <= 0:
        blue_timer = 0.0
        blue_game_over = True
        return

    if cap is None or recognizer is None:
        return
    ret, frame = cap.read()
    if ret:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = rgb_frame.shape
        preview_h = int(h * (240 / w))
        preview_small = cv2.resize(rgb_frame, (240, preview_h))
        camera_surface = pygame.image.frombuffer(preview_small.tobytes(), (240, preview_h), "RGB")
    else:
        detected_gesture = None
        return

    # 1. 展示階段：輪流顯示手勢圖片
    if current_gesture is not None:
        show_timer += dt
        if show_timer >= 2.0:
            show_timer = 0.0
            show_index += 1
            if show_index < len(gesture_sequence):
                current_gesture = gesture_sequence[show_index]
            else:
                current_gesture = None
        return

    # 2. 作答階段（圖片已消失）：讀取鏡頭並辨識手勢
    wait_timer += dt
    ret, frame = cap.read()
    if not ret:
        detected_gesture = None
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = rgb_frame.shape
    preview_h = int(h * (240 / w))
    preview_small = cv2.resize(rgb_frame, (240, preview_h))
    camera_surface = pygame.image.frombuffer(preview_small.tobytes(), (240, preview_h), "RGB")

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    result = recognizer.recognize(mp_image)
    if result.gestures and len(result.gestures[0]) > 0:
        detected_gesture = result.gestures[0][0].category_name
    else:
        detected_gesture = None

    # 3. 超過 2 秒準備時間後，比對目前要答的手勢
    if wait_timer >= 2.0 and detected_gesture is not None:
        target_name = gesture_sequence[answer_index][1]
        print("要答:", target_name, "| 辨識:", detected_gesture)
        if detected_gesture == target_name:
            answer_index += 1
            play_blue_correct_sfx()
            wait_timer = 0.0
            if answer_index >= len(gesture_sequence):
                score += 1
                stage_blue_start()
        else:
            stage_blue_start()
    # 4. 星星動畫
    star_pool = [img for img in (img_blue_grey_star, img_blue_light_star) if img is not None]
    star_spawn_timer += dt
    if len(star_pool) > 0 and len(blue_stars) < 3 and star_spawn_timer >= 2.2:
        star_spawn_timer = 0.0
        side = random.choice(["left", "right"])
        star_img = random.choice(star_pool)
        w = star_img.get_width()
        cam_top = SCREEN_H - (camera_surface.get_height() if camera_surface is not None else 180) - 25
        max_star_y = max(120, cam_top - star_img.get_height() - 20)
        y = random.randint(120, max_star_y)

        if side == "left":
            x = -w
        else:
            x = SCREEN_W
        blue_stars.append({"img": star_img, "side": side, "x": float(x), "y": float(y), "state": "out", "hold": 0.4})

    for s in blue_stars[:]:
        out_speed = 180.0
        in_speed = 420.0
        w = s["img"].get_width()
        if s["side"] == "left":
            target_out_x = -w * 0.35
            target_in_x = -w
            if s["state"] == "out":
                s["x"] = min(target_out_x, s["x"] + out_speed * dt)
                if s["x"] >= target_out_x:
                    s["state"] = "hold"
            elif s["state"] == "hold":
                s["hold"] -= dt
                if s["hold"] <= 0:
                    s["state"] = "in"
            else:
                s["x"] -= in_speed * dt
                if s["x"] <= target_in_x:
                    blue_stars.remove(s)
        else:
            target_out_x = SCREEN_W - w * 0.65
            target_in_x = float(SCREEN_W)
            if s["state"] == "out":
                s["x"] = max(target_out_x, s["x"] - out_speed * dt)
                if s["x"] <= target_out_x:
                    s["state"] = "hold"
            elif s["state"] == "hold":
                s["hold"] -= dt
                if s["hold"] <= 0:
                    s["state"] = "in"
            else:
                s["x"] += in_speed * dt
                if s["x"] >= target_in_x:
                    blue_stars.remove(s)



def stage_blue_draw(screen):
    global blue_timer, blue_stars, blue_game_over
    load_assets()
    pgz_game.screen = screen
    screen.blit(img_blue_bg, (0, 0))
    for s in blue_stars:
            screen.blit(s["img"], (int(s["x"]), int(s["y"])))
    if current_gesture is not None:
        screen.blit(current_gesture[0], (25, 25))
    if camera_surface is not None:
        screen.blit(camera_surface, (25, SCREEN_H - camera_surface.get_height() - 15))
    if current_gesture is None and len(gesture_sequence) > 0:
        step_text = f"{min(answer_index + 1, len(gesture_sequence))} / {len(gesture_sequence)}"
        font = pygame.font.SysFont("Avenir, Helvetica Neue, Arial", 96, bold=True)
        text_surf = font.render(step_text, True, (0, 0, 255))
        text_rect = text_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
        screen.blit(text_surf, text_rect)
    score_font = pygame.font.SysFont("Avenir,Helvetica Neue,Arial", 48, bold=True)
    score_surf = score_font.render(f"Score: {score}", True, (0, 0, 255))
    screen.blit(score_surf, (25, 200))
    timer_font = pygame.font.SysFont("Avenir,Helvetica Neue,Arial", 42, bold=True)
    timer_surf = timer_font.render(f"Time: {int(blue_timer) + 1 if blue_timer > 0 else 0}", True, (0, 0, 255))
    screen.blit(timer_surf, (25, 250))

    if blue_game_over:
        screen.fill((0, 0, 0))

        title_font = pygame.font.SysFont("Avenir,Helvetica Neue,Arial", 72, bold=True)
        title_surf = title_font.render("Time's Up!", True, (80, 180, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 110)))

        final_font = pygame.font.SysFont("Avenir,Helvetica Neue,Arial", 54, bold=True)
        final_surf = final_font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(final_surf, final_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 15)))

        blue_home_btn_rect.topleft = (SCREEN_W // 2 - 120, SCREEN_H // 2 + 80)

        target_surf = screen.surface if hasattr(screen, "surface") else screen
        pygame.draw.rect(target_surf, (80, 180, 255), blue_home_btn_rect, border_radius=12)


        btn_font = pygame.font.SysFont("Avenir,Helvetica Neue,Arial", 36, bold=True)
        btn_surf = btn_font.render("Home", True, (0, 0, 0))
        screen.blit(btn_surf, btn_surf.get_rect(center=blue_home_btn_rect.center))
        return


    



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
