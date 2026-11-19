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
    PATH_STAGE_RED_RUNNING_1,
    PATH_STAGE_RED_RUNNING_2,
    PATH_STAGE_RED_RUNNING_3,
    PATH_STAGE_RED_RUNNING_4,
    PATH_STAGE_RED_RUNNING_5,
    PATH_STAGE_RED_RUNNING_6,
    PATH_STAGE_RED_RUNNING_7,
    PATH_RED_BG,
    PATH_VOLUME_UP,
    PATH_VOLUME_DOWN,
    PATH_ONE,
    PATH_TWO,
    PATH_THREE,
    SCREEN_H,
    SCREEN_W,
    PATH_STAGE_RED_BG_MUSIC,

)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Red Stage")
    clock = pygame.time.Clock()

asset_root = Path(__file__).resolve().parent.parent / "assets"
loaders.set_root(str(asset_root))

run_frame_paths = (
    PATH_STAGE_RED_RUNNING_1,
    PATH_STAGE_RED_RUNNING_2,
    PATH_STAGE_RED_RUNNING_3,
    PATH_STAGE_RED_RUNNING_4,
    PATH_STAGE_RED_RUNNING_5,
    PATH_STAGE_RED_RUNNING_6,
    PATH_STAGE_RED_RUNNING_7,
)
run_frame_images = [
    Path(path).relative_to(Path("assets") / "images").with_suffix("").as_posix()
    for path in run_frame_paths
]
img_red_bg = None
bg_w = 0
bg_h = 0
bg_x1 = 0
bg_x2 = 0
bg_scroll_speed = 2

img_volume_up = None
img_volume_down = None
img_countdown_three = None
img_countdown_two = None
img_countdown_one = None
runner = None
countdown_elapsed = 0.0
COUNTDOWN_DURATION = 4.0

#set timer
total_time = 60.0
timer = total_time
timer_started = False

score = 0
game_over = False

rects = []
#rect_spawn_interval = 2.0
rect_spawn_timer = 0.0
current_spawn_interval = 2.0

velocity_y = 0
gravity = 1

#mirophone setting
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

VOL_MIN = 3
VOL_MAX = 180
VOL_RELEASE = VOL_MIN * 0.7
JUMP_MIN = 5
JUMP_MAX = 40

p = None
stream = None
smoothed_volume = 0.0
mic_opened = False
sound_trigger_armed = True

RECT_HEIGHT = 500
MAX_RECT_WIDTH = 700
MIN_RECT_WIDTH = 200
MIN_RECT_SPAWN_INTERVAL = 0.5
MAX_RECT_SPAWN_INTERVAL = 2.0
RECT_SPEED = 20
RECT_Y = 600
RECT_COLOR = (0, 0, 0)



class MovingRect:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.scored = False  # Flag to track if the rectangle has been scored

    def update(self):
        self.x -= self.speed
        

    def draw(self, screen):
        surface = getattr(screen, "surface", screen)
        pygame.draw.rect(surface, RECT_COLOR, (self.x, self.y, self.width, self.height))

music_started = False
def stage_red_enter():
    global p, stream, mic_opened
    if not mic_opened:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        mic_opened = True
        

def start_stage_red_music():
    global music_started
    if not music_started:
        pygame.mixer.music.load(PATH_STAGE_RED_BG_MUSIC)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        music_started = True


def stage_red_exit():
    global music_started, p, stream, mic_opened, smoothed_volume, sound_trigger_armed
    pygame.mixer.music.stop()
    music_started = False

    if stream is not None:
        stream.stop_stream()
        stream.close()
        stream = None
    if p is not None:
        p.terminate()
        p = None
    mic_opened = False
    smoothed_volume = 0.0
    sound_trigger_armed = True


def load_assets():
    global img_red_bg, img_volume_up, img_volume_down, runner, timer_font
    global img_countdown_three, img_countdown_two, img_countdown_one
    global bg_w, bg_h, bg_x2

    if runner is not None:
        return

    img_red_bg = pygame.image.load(PATH_RED_BG).convert_alpha()
    bg_w = img_red_bg.get_width()
    bg_h = img_red_bg.get_height()
    bg_x2 = bg_w
    img_volume_up = pygame.image.load(PATH_VOLUME_UP).convert_alpha()
    img_volume_down = pygame.image.load(PATH_VOLUME_DOWN).convert_alpha()
    img_countdown_three = pygame.image.load(PATH_THREE).convert_alpha()
    img_countdown_two = pygame.image.load(PATH_TWO).convert_alpha()
    img_countdown_one = pygame.image.load(PATH_ONE).convert_alpha()
    img_volume_up = pygame.transform.smoothscale(img_volume_up, (63, 450))
    img_volume_down = pygame.transform.smoothscale(img_volume_down, (63, 450))

    runner = Actor(run_frame_images[0], pos=(215, 529))
    runner.images = run_frame_images
    runner.fps = 12
    runner.scale = 0.2

    timer_font = pygame.font.Font(None, 36)


def stage_red_start():
    global timer, timer_started, score, game_over, velocity_y, smoothed_volume, sound_trigger_armed
    global countdown_elapsed, music_started
    load_assets()
    pygame.mixer.music.stop()
    music_started = False
    stage_red_enter()
    timer = total_time
    timer_started = True
    score = 0
    game_over = False
    velocity_y = 0
    runner.y = RECT_Y - runner.height / 2
    smoothed_volume = 0.0
    sound_trigger_armed = True
    countdown_elapsed = 0.0

    global rects, rect_spawn_timer, current_spawn_interval
    rects = []
    rect_spawn_timer = 0.0
    current_spawn_interval = random.uniform(MIN_RECT_SPAWN_INTERVAL, MAX_RECT_SPAWN_INTERVAL)
    started_floor = MovingRect(0, RECT_Y, 1500, RECT_HEIGHT, RECT_SPEED)
    rects.append(started_floor)

def get_current_volume():
    global smoothed_volume
    if stream is None:
        return 0.0
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_np = np.frombuffer(data, dtype=np.int16)
        rms = float(np.sqrt(np.mean(np.square(audio_np.astype(np.float32)))))
        smoothed_volume = 0.2 * smoothed_volume + 0.8 * rms
        return smoothed_volume
    except Exception as e:
        print(f"Error reading microphone data: {e}")
        return 0.0

def discard_microphone_chunk():
    if stream is not None:
        try:
            stream.read(CHUNK, exception_on_overflow=False)
        except Exception as e:
            print(f"Error reading microphone data: {e}")

def volume_to_jump_height(volume):
    vol_clamped = max(VOL_MIN, min(VOL_MAX, volume))
    ratio = (vol_clamped - VOL_MIN) / (VOL_MAX - VOL_MIN)
    jump_height = JUMP_MIN + ratio * (JUMP_MAX - JUMP_MIN)
    return jump_height

def update_background():
    global bg_x1, bg_x2
    bg_x1 -= bg_scroll_speed
    bg_x2 -= bg_scroll_speed
    if bg_x1 + bg_w < 0:
        bg_x1 = bg_x2 + bg_w
    if bg_x2 + bg_w < 0:
        bg_x2 = bg_x1 + bg_w

def stage_red_update(dt):
    global jump_height, score, game_over, velocity_y, timer, timer_started, rect_spawn_timer, current_spawn_interval
    global sound_trigger_armed, countdown_elapsed
    load_assets()

    if countdown_elapsed < COUNTDOWN_DURATION:
        discard_microphone_chunk()
        update_background()
        if countdown_elapsed + dt >= COUNTDOWN_DURATION - 1e-9:
            countdown_elapsed = COUNTDOWN_DURATION
        else:
            countdown_elapsed += dt
        return

    if game_over:
        return

    start_stage_red_music()
    runner.animate()

    if timer_started:
        timer -= dt
        if timer <= 0:
            timer = 0
            timer_started = False

    for rect in rects:
        rect.update()
    #spawn new rectangles
    rect_spawn_timer += dt
    if rect_spawn_timer >= current_spawn_interval and not game_over:
        rect_spawn_timer = 0.0
        rect_width = random.randint(MIN_RECT_WIDTH, MAX_RECT_WIDTH)
        rect_x = SCREEN_W
        new_rect = MovingRect(rect_x, RECT_Y, rect_width, RECT_HEIGHT, RECT_SPEED)
        rects.append(new_rect)
        current_spawn_interval = random.uniform(MIN_RECT_SPAWN_INTERVAL, MAX_RECT_SPAWN_INTERVAL)

    on_floor = False
    runner_bottom_y = runner.y + runner.height / 2
    runner_left = runner.x - runner.width / 2
    runner_right = runner.x + runner.width / 2
    for rect in rects:
        rect_left = rect.x
        rect_right = rect.x + rect.width
        if not (runner_right < rect_left or runner_left > rect_right):
            if abs(runner_bottom_y - rect.y) <= 1:
                on_floor = True
                break

    vol = get_current_volume()
    jump_height = volume_to_jump_height(vol)

    if vol <= VOL_RELEASE:
        sound_trigger_armed = True
    elif vol > VOL_MIN and sound_trigger_armed:
        sound_trigger_armed = False
        if on_floor and not game_over:
            velocity_y = -jump_height
    
    if not game_over:
        previous_bottom_y = runner.y + runner.height / 2
        velocity_y += gravity
        runner.y += velocity_y
        next_bottom_y = runner.y + runner.height / 2

        if velocity_y > 0:
            for rect in rects:
                rect_left = rect.x
                rect_right = rect.x + rect.width
                overlaps_horizontally = not (runner_right < rect_left or runner_left > rect_right)
                crossed_platform_top = previous_bottom_y <= rect.y <= next_bottom_y
                if overlaps_horizontally and crossed_platform_top:
                    runner.y = rect.y - runner.height / 2
                    velocity_y = 0
                    break

        if runner.y + runner.height / 2 >= SCREEN_H:
            game_over = True
            timer_started = False
            return

    # add score
    runner_left = runner.x - runner.width / 2
    for rect in rects:
        rect_right_x = rect.x + rect.width
        if rect_right_x < runner_left and not rect.scored:
            score += 1
            rect.scored = True

    update_background()
    
        




def stage_red_draw(screen):
    load_assets()
    screen.blit(img_red_bg, (bg_x1, 0))
    screen.blit(img_red_bg, (bg_x2, 0))
    pgz_game.screen = screen

    if countdown_elapsed < COUNTDOWN_DURATION:
        for rect in rects:
            rect.draw(screen)
        if not game_over:
            runner.draw()

        countdown_image = None
        if countdown_elapsed < 1.0:
            countdown_image = img_countdown_three
        elif countdown_elapsed < 2.0:
            countdown_image = img_countdown_two
        elif countdown_elapsed < 3.0:
            countdown_image = img_countdown_one
        if countdown_image is not None:
            screen.blit(countdown_image, (0, 0))
        return

    screen.blit(img_volume_down, (930,60))
    screen.blit(img_volume_up, (930,60))

    sec = int(timer)
    m = sec // 60
    s = sec % 60
    timer_text = timer_font.render(f"Time: {m:02d}:{s:02d}", True, (255, 255, 255))
    screen.blit(timer_text, (20, 20))

    score_text = timer_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 60))

    for rect in rects:
        rect.draw(screen)

    if not game_over:
        runner.draw()

    


if __name__ == "__main__":
    running = True
    stage_red_start()
    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keyboard._press(event.key)
            elif event.type == pygame.KEYUP:
                keyboard._release(event.key)
        stage_red_update(dt)
        stage_red_draw(screen)
        pygame.display.flip()
    pygame.quit()