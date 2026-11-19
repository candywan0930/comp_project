import pygame

SCREEN_W = 1024
SCREEN_H = 768
FPS = 60

MAX_WEIGHT = 255
r_weight = 0
g_weight = 0
b_weight = 0

IDLE_TIMEOUT = 30
IDLE_TIP_TIMES = [10,20]

STATE_HOME = "home"
STATE_LOADING = "loading"
STATE_RED = "red"
STATE_GREEN = "green"
STATE_BLUE = "blue"
STATE_END_LOST = "end_lost"
STATE_END_MAIN = "end_main"
#photo
#home page
PATH_HOME_BG = "assets/images/home_bg.png"
PATH_HAIRDRY_BW = "assets/images/hairdry_bw.png"
PATH_HAIRDRY_R = "assets/images/hairdry_r.png"
PATH_LAMP_B = "assets/images/lamp_b.png"
PATH_LAMP_BW = "assets/images/lamp_bw.png"
PATH_PLANT_G = "assets/images/plant_g.png"
PATH_PLANT_BW = "assets/images/plant_bw.png"
PATH_WASH = "assets/images/wash.png"
PATH_POINTER = "assets/images/pointer.png"
PATH_MIRROR_BG = "assets/images/mirror_bg.png"
#stage red
PATH_RED_BG = "assets/images/stage_red_BG.png"
PATH_STAGE_RED_RUNNING_1 = "assets/images/stage_red_running/stage_red_running_1.png"
PATH_STAGE_RED_RUNNING_2 = "assets/images/stage_red_running/stage_red_running_2.png"
PATH_STAGE_RED_RUNNING_3 = "assets/images/stage_red_running/stage_red_running_3.png"
PATH_STAGE_RED_RUNNING_4 = "assets/images/stage_red_running/stage_red_running_4.png"
PATH_STAGE_RED_RUNNING_5 = "assets/images/stage_red_running/stage_red_running_5.png"
PATH_STAGE_RED_RUNNING_6 = "assets/images/stage_red_running/stage_red_running_6.png"
PATH_STAGE_RED_RUNNING_7 = "assets/images/stage_red_running/stage_red_running_7.png"
PATH_VOLUME_UP = "assets/images/volume_up.png"
PATH_VOLUME_DOWN = "assets/images/volume_down.png"


# stage green
PATH_FAIL_OPEN_PALM_GREEN_CHAR = "assets/images/fail_open_palm_green_character.png"
PATH_GREEN_BACKGROUND = "assets/images/green_background.png"
PATH_CLOSED_PALM_LEAVES_GREEN_CHAR = "assets/images/closed_palm_leaves_green_character.png"
PATH_GREEN_WORM = "assets/images/green_worm.png"
PATH_STAGE_GREEN_LEAF = "assets/images/stage_green_leaf.png"
PATH_OPEN_PALM_GREEN_CHAR = "assets/images/open_palm_green_character.png"

# stage blue
PATH_STAGE_BLUE_BG = "assets/images/stage_blue_bg.png"
PATH_BLUE_BAD = "assets/images/blue_bad.png"
PATH_BLUE_POINTING = "assets/images/blue_pointing.png"
PATH_BLUE_FIST = "assets/images/blue_fist.png"
PATH_BLUE_ILOVEU = "assets/images/blue_iloveu.png"
PATH_BLUE_VICTORY = "assets/images/blue_victory.png"
PATH_BLUE_OPENHAND = "assets/images/blue_openhand.png"
PATH_BLUE_GOOD = "assets/images/blue_good.png"
PATH_STAGE_BLUE_GREY_STAR = "assets/images/stage_blue_greystar.png"
PATH_STAGE_BLUE_LIGHT_STAR = "assets/images/stage_blue_lightstar.png"


#other
PATH_ONE = "assets/images/one.png"
PATH_TWO = "assets/images/two.png"
PATH_THREE = "assets/images/three.png"

#music
PATH_HOME_BG_MUSIC = "assets/audio/home_bg_music.wav"
PATH_STAGE_RED_BG_MUSIC = "assets/audio/stage_red_bg.wav"