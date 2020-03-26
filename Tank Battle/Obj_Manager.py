import sys, time, math, random, pygame
import Function_Set as func
from pygame.locals import *


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

    def to_int(self):
        self.x = int(self.x)
        self.y = int(self.y)


class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        # extend the base Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.master_image = None
        self.scratch = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.rect = None
        self.rotation = 0
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
            if current_time > self.last_time + rate:
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


class Tank(MySprite):
    def __init__(self, tank_file="tank.png", turret_file="turret.png"):
        MySprite.__init__(self)
        self.load(tank_file, 50, 60, 4)
        self.speed = 0.0
        self.scratch = None
        self.float_pos = Point(0, 0)
        self.velocity = Point(0, 0)
        self.turret = MySprite()
        self.turret.load(turret_file, 32, 64, 4)
        self.first_timer = 0
        self.rotation = 0
        self.fire = False
        self.fire_timer = 0
        self.live = 100

    def reset(self):
        self.rotation = random.randint(0, 360)
        self.live = 100
        self.float_pos = Point(random.randint(50, 760), random.randint(50, 560))

    def update(self, ticks, rate=30):
        MySprite.update(self, ticks, rate)
        self.rotation = func.wrap_angle(self.rotation)
        self.scratch = pygame.transform.rotate(self.image, -self.rotation)
        angle = func.wrap_angle(self.rotation-90)
        self.velocity = func.angular_velocity(angle)
        self.float_pos.x += self.velocity.x
        self.float_pos.y += self.velocity.y

        # wrap tank around screen edges (keep it simple)
        '''if self.float_pos.x < 0: self.float_pos.x = 0
        elif self.float_pos.x > 800: self.float_pos.x = 800
        if self.float_pos.y < 0: self.float_pos.y = 0
        elif self.float_pos.y > 600: self.float_pos.y = 600'''
        if not 0 < self.float_pos.x < 800 or not 0 < self.float_pos.y < 600:
            self.rotation -= 100

        # transfer float position to integer position for drawing
        self.X = int(self.float_pos.x)
        self.Y = int(self.float_pos.y)

        # update turret
        self.turret.position = (self.X, self.Y)
        self.turret.last_frame = 0
        self.turret.update(ticks, 60)
        self.turret.rotation = func.wrap_angle(self.turret.rotation)
        angle = self.turret.rotation + 90
        self.turret.scratch = pygame.transform.rotate(self.turret.image, -angle)
        if self.live < 0:
            self.reset()

    def draw(self, surface):
        width, height = self.scratch.get_size()
        center = Point(width//2, height//2)
        surface.blit(self.scratch, (self.X-center.x, self.Y-center.y))

        width, height = self.turret.scratch.get_size()
        center = Point(width//2, height//2)
        surface.blit(self.turret.scratch, (self.turret.X-center.x, self.turret.Y-center.y))

        if self.live > 70: live_color = (0, 0, 255)
        elif self.live > 30: live_color = (255, 255, 0)
        else: live_color = (255, 0, 0)
        live_width, live_height = self.scratch.get_size()
        top = self.position[0] - live_width//2 - 20
        left = self.position[1] - live_height//2
        live_width += 40
        pygame.draw.rect(surface, (255, 255, 255), (top, left-20, live_width, 20), 2)
        pygame.draw.rect(surface, live_color, (top+2, left-20+3, (live_width-4)*(self.live/100), 15), 0)

    def __str__(self):
        return MySprite.__str__(self) + "," + str(self.velocity)


class EnemyTank(Tank):
    def __init__(self, tank_file="enemy_tank.png", turret_file="enemy_turret.png"):
        Tank.__init__(self, tank_file, turret_file)
        self.timer = 0

    def auto_attack(self, player):
        self.turret.rotation = func.target_angle(self.turret.position[0], self.turret.position[1],
                                                 player.turret.position[0], player.turret.position[1])

    def update(self, ticks, rate=30):
        Tank.update(self, ticks, rate)


class Bullet:
    def __init__(self, position):
        self.alive = True
        self.color = (250, 20, 20)
        self.position = Point(position.x, position.y)
        self.velocity = Point(0, 0)
        self.rect = Rect(0, 0, 4, 4)
        self.owner = ""

    def update(self, ticks):
        self.position.x += self.velocity.x * 10.0
        self.position.y += self.velocity.y * 10.0
        if not 0 < self.position.x < 800 or not 0 < self.position.y < 600:
            self.alive = False
        self.rect = Rect(self.position.x, self.position.y, 4, 4)

    def draw(self, surface):
        self.position.to_int()
        if self.owner == "player":
            self.color = (0, 255, 0)
        else:
            self.color = (255, 0, 0)
        pygame.draw.circle(surface, self.color, (self.position.x, self.position.y), 4, 0)




