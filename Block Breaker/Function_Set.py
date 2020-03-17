import sys
import time
import pygame
import random
import math
from pygame.locals import *


class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        # extend the base Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.rect = None
        self.direction = 0
        self.velocity = Point(0, 0)
    # X property
    def _getx(self): return self.rect.x
    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    # Y property
    def _gety(self): return self.rect.y
    def _sety(self, value): self.rect.y = value
    Y = property(_gety, _sety)

    # position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self, pos): self.rect.topleft = pos
    position = property(_getpos, _setpos)

    def load(self, filename, width=0, height=0, columns=1):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.set_image(self.master_image, width, height, columns)

    def set_image(self, image, width=0, height=0, columns=1):
        self.master_image = image
        if width == 0 and height == 0:
            self.frame_width = image.get_width()
            self.frame_height = image.get_height()
        else:
            self.frame_width = width
            self.frame_height = height
            rect = self.master_image.get_rect()
            self.last_frame = (rect.width//width)*(rect.height//height) - 1
        self.rect = Rect(0, 0, self.frame_width, self.frame_height)
        self.columns = columns

    def update(self, current_time, rate=30):
        # update animation frame number
        if self.last_frame > self.first_frame:
            # update animation frame number
            if cureent_time > self.last_time + rate:
                self.frame += 1
                if self.frame > self.last_frame:
                    self.frame = self.first_frame
                self.last_time = current_time
        else:
            self.frame = self.first_frame

        # build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str(self):
        return str(self.name) + "," + str(self.first_frame) + \
                "," + str(self.last_frame_ + "," + str(self.frame_width)) + \
                "," + str(self.frame_height) + "," + str(self.columns) + \
                "," + str(self.rect)


def print_text(font__, x, y, text, color__=(255, 255, 255)):
    imgtext = font__.render(text, True, color__)
    screen = pygame.display.get_surface()
    screen.blit(imgtext, (x, y))


class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # X property
    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    x = property(getx, setx)

    # Y property
    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{.0f}".format(self.__x) +\
                ", Y:" + "{.0f}".format(self.__y) + "}"
