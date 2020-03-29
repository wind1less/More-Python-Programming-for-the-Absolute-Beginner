import sys, time, math, random, pygame
from pygame.locals import *
import Function_Set as func

global terrain


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


class Terrain:
    def __init__(self, min_height, max_height, total_points):
        self.min_height = min_height
        self.max_height = max_height
        self.total_points = total_points + 1
        self.grid_size = 800 / total_points
        self.height_map = list()
        self.grid_point = 0
        self.generate()

    def generate(self):
        if len(self.height_map): self.height_map.clear()
        last_height = (self.max_height+self.min_height) // 2
        self.height_map.append(last_height)
        direction = 1
        run_length = True
        for n in range(self.total_points):
            rand_dist = random.randint(1, 10) * direction
            height = last_height + rand_dist
            self.height_map.append(int(height))
            if height < self.min_height: direction = 1
            elif height > self.max_height: direction = -1
            last_height = height
            if run_length:
                run_length = False
                direction = random.choice([-1, 1])
            else:
                run_length = -True

    def set_grid_point(self, grid_point):
        self.grid_point = grid_point

    def get_height(self, x):
        if x > 800:
            return 0
        elif x <= 0:
            return 0
        grid_point = int(x / self.grid_size)
        return self.height_map[grid_point]

    def draw(self, surface):
        last_x = 0
        for n in range(1, self.total_points):
            height = 600 - self.height_map[n]
            x_pos = int(n * self.grid_size)
            pos = (x_pos, height)
            color__ = (255, 255, 255)
            if n == self.grid_point:
                func.draw_crosshair(surface, (pos[0], pos[1]-10))
            last_height = 600 - self.height_map[n-1]
            last_pos = (last_x, last_height)
            pygame.draw.line(surface, color__, last_pos, pos, 2)
            last_x = x_pos


class Cannon:
    def __init__(self, angle, color__, turret_color, position, rand_power=True):
        self.color = color__
        self.position = position
        self.turret_color = turret_color
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)
        self.angle = angle
        self.live = 100
        self.rand_power = rand_power
        if rand_power:
            self.power = random.randint(5, 15)
        else:
            self.power = 5

    def draw(self, surface):
        if self.rand_power:
            self.power = random.randint(5, 15)
        start_x = self.position.x + 15
        start_y = self.position.y + 0
        self.start_pos = (start_x, start_y)
        vel = func.angular_velocity(func.wrap_angle(self.angle-90))
        self.end_pos = (start_x + vel.x*30, start_y + vel.y * 30)
        pygame.draw.line(surface, self.turret_color, self.start_pos, self.end_pos, 6)
        rect = Rect(self.position.x, self.position.y, 30, 30)
        pygame.draw.rect(surface, (255, 255, 255), Rect(self.position.x, self.position.y-30, 30, 5), 1)
        pygame.draw.rect(surface, self.color, Rect(self.position.x+1, self.position.y-29, (self.live/100)*28, 3), 0)
        pygame.draw.rect(surface, self.color, rect, 0)
        pygame.draw.circle(surface, self.color, (int(self.position.x+15), int(self.position.y+0)), 15, 0)


class Shell(MySprite):
    def __init__(self, owner, cannon, power):
        MySprite.__init__(self)
        self.owner = owner
        self.angle = 0
        self.velocity = Point(0, 0)
        self.boom = False
        if owner == "computer":
            color__ = (230, 30, 30)
        else:
            color__ = (30, 230, 30)

        image = pygame.Surface((8, 8))
        pygame.draw.circle(image, color__, (4, 4), 4, 0)
        self.set_image(image)

        self.angle = func.wrap_angle(cannon.angle - 90)
        self.velocity = func.angular_velocity(self.angle)
        self.velocity.x *= power
        self.velocity.y *= power
        self.X = cannon.end_pos[0] + 5
        self.Y = cannon.end_pos[1] - 5

    def update(self, current_time, terrain, rate=30):
        MySprite.update(self, current_time, rate)
        self.X += self.velocity.x
        self.Y += self.velocity.y
        if self.velocity.y < 10.0:
            self.velocity.y += 0.1
        height = 600 - terrain.get_height(self.X)
        if self.Y > height:
            self.boom = True
        elif not 0 < self.X < 800:
            self.boom = True
        elif not 0 < self.Y < 600:
            self.boom = True





















































