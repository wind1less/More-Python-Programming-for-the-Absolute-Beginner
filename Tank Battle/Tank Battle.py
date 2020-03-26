import sys, time, math, random, pygame
import Function_Set
import Obj_Manager
from Function_Set import *
from pygame.locals import *
from Obj_Manager import *

# initialize game n' parameters
screen_width = 800
screen_height = 600
caption = "Tank Battle Game"
screen = game_initialize(screen_width, screen_height, caption, False)
backbuffer = pygame.Surface((800, 600))
font = pygame.font.SysFont("Arial", 24)
timer = pygame.time.Clock()
game_over = False
player_score = 0
enemy_score = 0
last_time = 0
mouse_x, mouse_y = 0, 0
fps = 60

# initializes the audio system
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("shoot.wav")
boom_sound = pygame.mixer.Sound("boom.wav")

# load mouse cursor
crosshair = MySprite()
crosshair.load("crosshair.png")
crosshair_group = pygame.sprite.GroupSingle()
crosshair_group.add(crosshair)

# create player tank
player = Tank()
player.float_pos = Point(400, 500)

# create enemy tanks
enemy_tank = EnemyTank()
enemy_tank.float_pos = Point(random.randint(50, 760), 50)
enemy_tank.rotation = 135

# create bullets
bullets = list()

while True:
    timer.tick(fps)
    ticks = pygame.time.get_ticks()

    # reset mouse state variables
    mouse_up = mouse_down = 0
    mouse_up_x = mouse_up_y = mouse_down_x = mouse_down_y = 0

    # event section
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            move_x, move_y = event.rel
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = event.button
            mouse_down_x, mouse_down_y = event.pos
        elif event.type == MOUSEBUTTONUP:
            mouse_up = event.button
            mouse_up_x, mouse_up_y = event.pos

    # get key states
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_LEFT] or keys[K_a]:
        player.rotation -= 2.0
    elif keys[K_RIGHT] or keys[K_d]:
        player.rotation += 2.0

    # fire cannon
    if keys[K_SPACE] or mouse_up > 0:
        if ticks > player.fire_timer + 500:
            player.fire_timer = ticks
            player.fire = True
            fire_cannon(player, bullets, "player", shoot_sound)
    else:
        player.fire = False

    # update section
    if not game_over:
        crosshair.position = (mouse_x, mouse_y)
        crosshair_group.update(ticks)

    # point tank turret toward crosshair
    crosshair_center_x = crosshair.X + crosshair.frame_width/2
    crosshair_center_y = crosshair.Y + crosshair.frame_height/2
    angle = target_angle(player.turret.X, player.turret.Y, crosshair_center_x, crosshair_center_y)
    player.turret.rotation = angle

    # move tank
    player.update(ticks)
    enemy_tank.update(ticks)

    if ticks > enemy_tank.fire_timer + 500:
        enemy_tank.fire_timer = ticks
        fire_cannon(enemy_tank, bullets, "enemy", shoot_sound)
        enemy_tank.fire = True
    else:
        enemy_tank.fire = False

    if ticks > enemy_tank.timer + 1500:
        enemy_tank.timer = ticks
        enemy_tank.auto_attack(player)

    # update bullets
    for bullet in bullets:
        bullet.update(ticks)
        if bullet.owner == "player":
            if pygame.sprite.collide_rect(bullet, enemy_tank):
                player_score += 1
                enemy_tank.live -= 1
                bullet.alive = False
                play_sound(boom_sound)
        elif bullet.owner == "enemy":
            if pygame.sprite.collide_rect(bullet, player):
                enemy_score += 1
                player.live -= 1
                bullet.alive = False
                play_sound(boom_sound)

    # drawing section
    backbuffer.fill((100, 200, 20))

    # remove expired bullets
    for bullet in bullets:
        if not bullet.alive:
            bullets.remove(bullet)
        else:
            bullet.draw(backbuffer)

    enemy_tank.draw(backbuffer)
    player.draw(backbuffer)
    crosshair_group.draw(backbuffer)

    screen.blit(backbuffer, (0, 0))

    print_text(font, 400, 20, "Turret Angle: " + "{:.2f}".format(player.turret.rotation))
    if not game_over:
        print_text(font, 0, 0, "PLAYER: " + str(player_score))
        print_text(font, 700, 0, "ENEMY: " + str(enemy_score))
    else:
        print_text(font, 0, 0, "GAME OVER")

    pygame.display.update()

