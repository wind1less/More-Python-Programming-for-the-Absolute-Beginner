import sys, time, math, random, pygame
import Obj_Manager
from pygame.locals import *
from Obj_Manager import *


def print_text(font__, x, y, text, color__=(255, 255, 255)):
    imgtext = font__.render(text, True, color__)
    screen = pygame.display.get_surface()
    screen.blit(imgtext, (x, y))


def angular_velocity(angle):
    vel = Point(0, 0)
    vel.x = math.cos(math.radians(angle))
    vel.y = math.sin(math.radians(angle))
    return vel


def target_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees


def wrap_angle(angle):
    return abs(angle % 360)


def play_sound(sound):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(sound)


def game_initialize(screen_width, screen_height, caption, mouse_visible=False):
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(caption)
    pygame.mouse.set_visible(mouse_visible)

    return screen


def fire_cannon(tank, bullets, owner, shoot_sound):
    position = Point(tank.turret.X, tank.turret.Y)
    bullet = Bullet(position)
    angle = tank.turret.rotation
    bullet.velocity = angular_velocity(angle)
    bullet.owner = owner
    bullets.append(bullet)
    play_sound(shoot_sound)
