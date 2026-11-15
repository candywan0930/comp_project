import cv2
import numpy as np
import pygame

pygame.init()
SCREEN_W, SCREEN_H = 1280, 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# 打开绿幕影片
cap = cv2.VideoCapture("green_video.mp4")

# 绿色HSV范围，你之后可以微调
lower_green = np.array([35, 60, 60])
upper_green = np.array([85, 255, 255])

running = True
while running:
    ret, frame = cap.read()
    if not ret:
        # 播完就从头循环
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    # 1. 抠绿幕
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # 反相mask：唔系绿色嘅地方先保留
    mask_inv = cv2.bitwise_not(mask)

    # 转RGBA，绿色区域alpha=0（透明）
    frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    frame_rgba[:, :, 3] = mask_inv

    # 2. opencv係BGR，pygame要RGBA，调转通道
    frame_rgba = cv2.cvtColor(frame_rgba, cv2.COLOR_BGRA2RGBA)
    # 转成pygame surface
    fg_surf = pygame.image.frombuffer(frame_rgba.tobytes(), frame_rgba.shape[1::-1], "RGBA")
    # 可以缩放影片大小
    fg_surf = pygame.transform.smoothscale(fg_surf, (400, 600))

    # -------- 绘图 --------
    # 底层背景（你可以换成你red stage嘅背景）
    screen.fill((60,0,0))
    # 画抠好嘅透明影片
    screen.blit(fg_surf, (100, 50))

    # 事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

cap.release()
pygame.quit()
