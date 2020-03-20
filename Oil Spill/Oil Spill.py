# Oil Spill Game

import sys, time, random, math, pygame
from pygame.locals import *
from Function_Set import *

global screen, bg_buffer, font, timer, oil_group, cursor, cursor_group
global new_oil, clean_oil


class OilSprite(MySprite):
    def __init__(self):
        MySprite.__init__(self)
        self.radius = random.randint(0, 60) + 30
        play_sound(new_oil)
        self.dire_x = random.choice([1, -1])
        self.dire_y = random.choice([1, -1])

    def update(self, timing, rate=30):
        MySprite.update(self, timing, rate)

    def fade(self):
        r2 = self.radius // 2
        color__ = self.image.get_at((r2, r2))
        if color__.a > 20:
            color__.a -= 5
            pygame.draw.circle(self.image, color__, (r2, r2), r2, 0)
        else:
            oil_group.remove(self)
            play_sound(clean_oil)

    def move(self):
        self.velocity = Point(12*self.dire_x, 12*self.dire_y)


# this function initializes the game
def game_init():
    global screen, bg_buffer, font, oil_group, cursor, cursor_group

    screen_width = 800
    screen_height = 600
    caption = "Oil Spill Game"
    screen = game_initialize(screen_width, screen_height, caption)
    font = pygame.font.SysFont("Arial", 24)

    # create a drawing surface
    bg_buffer = pygame.Surface((screen_width, screen_height))
    bg_buffer.fill(dark_tan)

    # create oil list
    oil_group = pygame.sprite.Group()

    # create cursor sprite
    cursor_group = pygame.sprite.Group()
    cursor = MySprite()
    cursor.radius = 60
    image = pygame.Surface((60, 60)).convert_alpha()
    image.fill((255, 255, 255, 0))
    pygame.draw.circle(image, (80, 80, 220, 70), (30, 30), 30, 0)
    pygame.draw.circle(image, (80, 80, 250, 255), (30, 30), 30, 4)
    cursor.set_image(image)
    cursor_group.add(cursor)


# this function initializes the audio system
def audio_init():
    global new_oil, clean_oil

    # initializes the audio mixer, load sound files
    pygame.mixer.init()
    new_oil = pygame.mixer.Sound("new_oil.wav")
    clean_oil = pygame.mixer.Sound("clean_oil.wav")


def play_sound(sound):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(sound)


def add_oil():
    global oil_group, new_oil

    oil__ = OilSprite()
    image = pygame.Surface((oil__.radius, oil__.radius)).convert_alpha()
    image.fill((255, 255, 255, 0))
    oil__.fade_level = random.randint(50, 150)
    oil_color = 10, 10, 20, oil__.fade_level
    r2 = oil__.radius // 2
    pygame.draw.circle(image, oil_color, (r2, r2), r2, 0)
    oil__.set_image(image)
    oil_group.add(oil__)
    oil__.X = random.randint(40, 760)
    oil__.Y = random.randint(40, 560)


# define variable
dark_tan = 190, 190, 110, 255
tan = 210, 210, 130, 255
last_time = 0
fps = 30

# main program begins
game_init()
audio_init()
game_over = False
fps = 30
timer = pygame.time.Clock()

oil_num = 0

# repeating loop
while True:
    timer.tick(fps)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()
    if len(oil_group) > 180: game_over = True
    # get mouse input
    button = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()
    pos = (mx+30, my+30)
    if button[0] > 0: pygame.draw.circle(bg_buffer, tan, pos, 30, 0)
    if not game_over:
        # collision test
        oil_hit = None
        for oil in oil_group:
            if pygame.sprite.collide_circle_ratio(0.5)(cursor, oil):
                oil_hit = oil
                if button[0] > 0:
                    oil_hit.fade()
                    break

        # add new oil sprite once per second
        if ticks > last_time + 1000:
            add_oil()
            last_time = ticks

        # draw back buffer
        screen.blit(bg_buffer, (0, 0))

        # draw oil
        oil_group.update(ticks)
        oil_group.draw(screen)

        # draw cursor
        cursor.position = (mx, my)
        cursor_group.update(ticks)
        cursor_group.draw(screen)

    oil_num = len(oil_group)
    print_text(font, 600, 0, "OIL: " + str(oil_num))
    if oil_hit: print_text(font, 0, 0, "OIL SPLOTCH - CLEAN IT!")
    else: print_text(font, 0, 0, "CLEAN")
    if game_over: print_text(font, 320, 200, "G A M E O V E R !")
    pygame.draw.line(screen, (0, 0, 255), (0, 30), (800, 30), 5)
    pygame.display.update()
