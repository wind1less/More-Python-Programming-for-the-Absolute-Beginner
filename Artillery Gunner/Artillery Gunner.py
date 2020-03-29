import sys, time, math, random, pygame
import Function_Set
import Obj_Manager
from pygame.locals import *
from Function_Set import *
from Obj_Manager import *

screen = game_initialize(800, 600, "Artillery Gunner", True)
backbuffer = pygame.Surface((800, 600))
font = pygame.font.SysFont("consolas", 20)
timer = pygame.time.Clock()
mouse_x, mouse_y = 0, 0
terrain = Terrain(100, 200, 20)
shell_group = pygame.sprite.Group()
pos = Point(0, 0)
game_over = False
pygame.mixer.music.load("heikong.mp3")
pygame.mixer.music.play()
pygame.mixer_music.set_volume(0.3)
shoot_sound = pygame.mixer.Sound("shoot.wav")
boom_sound = pygame.mixer.Sound("boom.wav")
bg_color = (20, 20, 120)

player_cannon = Cannon(45, (30, 220, 30), (30, 180, 30), pos, False)
player_position = Point(0, 0)
player_shell_num = 0
player_score = 0
player_live = 100
computer_live = 100

computer_cannon = Cannon(275, (220, 30, 30), (180, 30, 30), pos)
computer_position = Point(0, 0)
computer_shell_num = 0
computer_score = 0

while True:
    timer.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    if not game_over:
        if keys[K_SPACE]:
            if player_shell_num < 8:
                player_shell = Shell("player", player_cannon, player_cannon.power)
                shell_group.add(player_shell)
                play_sound(shoot_sound)
        if keys[K_UP]:
            player_cannon.angle -= 1
        elif keys[K_DOWN]:
            player_cannon.angle += 1
        elif keys[K_LEFT]:
            if player_cannon.power > 0:
                player_cannon.power -= 1
        elif keys[K_RIGHT]:
            if player_cannon.power < 20:
                player_cannon.power += 1
        player_shell_num = computer_shell_num = 0

        for shell in shell_group:
            if shell.owner == "computer":
                computer_shell_num += 1
                target_pos = player_cannon.position
            else:
                player_shell_num += 1
                target_pos = computer_cannon.position
            dist = distance(shell.position, target_pos)
            if dist < 25:
                bg_color = bg_color_reset()
                play_sound(boom_sound)
                shell.boom = True
                if shell.owner == "player":
                    computer_cannon.live -= 1
                    player_score += 1
                else:
                    player_cannon.live -= 1
                    computer_score += 1
            if shell.boom:
                shell_group.remove(shell)

        if computer_shell_num < 100:
            computer_cannon.angle = random.randint(270, 320)
            computer_shell = Shell("computer", computer_cannon, computer_cannon.power)
            shell_group.add(computer_shell)
            play_sound(shoot_sound)

        grid_point = int(mouse_x / terrain.grid_size)
        terrain.set_grid_point(grid_point)
        player_position = Point(terrain.grid_size*1, 600-terrain.height_map[1]-30)
        computer_position = Point(terrain.grid_size*19, 600-terrain.height_map[19]-30)
        player_cannon.position = player_position
        computer_cannon.position = computer_position

    backbuffer.fill(bg_color)
    terrain.draw(backbuffer)
    player_cannon.draw(backbuffer)
    computer_cannon.draw(backbuffer)
    shell_group.update(0, terrain)
    shell_group.draw(backbuffer)
    screen.blit(backbuffer, (0, 0))

    if player_cannon.live <= 0:
        game_over = True
        print_text(font, 360, 270, "You Lose!", (255, 255, 200))
    if computer_cannon.live <= 0:
        game_over = True
        print_text(font, 360, 270, "You Win!", (255, 255, 200))

    if not game_over:
        print_text(font, 5, 560, "Cursor Pos:  " + str(mouse_x) + "  " + str(mouse_y), (255, 0, 0))
        print_text(font, 250, 560, "Grid Point:  " + str(terrain.grid_point), (255, 0, 0))

        print_text(font, 5, 5, "Angle:" + "{:-6.2f}".format(player_cannon.angle), (255, 0, 0))
        print_text(font, 5, 25, "Score:" + "{:-6.2f}".format(player_score), (255, 0, 0))
        print_text(font, 5, 45, "Power:" + "{:-6.2f}".format(player_cannon.power), (255, 0, 0))
        print_text(font, 640, 5, "Angle:" + "{:-6.2f}".format(computer_cannon.angle), (255, 0, 0))
        print_text(font, 640, 25, "Score:" + "{:-6.2f}".format(computer_score), (255, 0, 0))
        print_text(font, 640, 45, "Power:" + "{:-6.2f}".format(computer_cannon.power), (255, 0, 0))

    pygame.display.update()
