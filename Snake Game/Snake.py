# Snake Game

import sys, time, random, math, pygame

from pygame.locals import *
from Function_Set import *

global head_x, head_y, step_time


class SnakeSegment(MySprite):
    def __init__(self, color__=(20, 200, 20)):
        MySprite.__init__(self)
        image__ = pygame.Surface((16, 16)).convert_alpha()
        image__.fill((255, 255, 255, 0))
        pygame.draw.rect(image__, color__, (0, 0, 16, 16), 4)
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.rect(image__, random_color, (4, 4, 8, 8), 0)
        self.set_image(image__)
        MySprite.update(self, 0, 60)


class Snake:
    def __init__(self):
        self.velocity = Point(0, 1)
        self.old_time = 0
        head__ = SnakeSegment((250, 250, 50))
        head__.X, head__.Y = 20*16, 10*16
        self.segments = list()
        self.segments.append(head__)
        self.add_segment()
        self.add_segment()

    def update(self, ticks__):
        global step_time
        if ticks > self.old_time + step_time:
            self.old_time = ticks__
            # move body segments
            for ss in range(len(self.segments)-1, 0, -1):
                self.segments[ss].X = self.segments[ss-1].X
                self.segments[ss].Y = self.segments[ss-1].Y
            # move snake head
            self.segments[0].X += self.velocity.x * 16
            self.segments[0].Y += self.velocity.y * 16

    def draw(self, surface):
        for segment in self.segments:
            surface.blit(segment.image, (segment.X, segment.Y))

    def add_segment(self):
        last = len(self.segments) - 1
        segment = SnakeSegment()
        start = Point(0, 0)
        if self.velocity.x < 0:
            start.x = 16
        elif self.velocity.x > 0:
            start.x = -16
        if self.velocity.y < 0:
            start.y = 16
        elif self.velocity.y > 0:
            start.y = -16
        segment.X = self.segments[last].X + start.x
        segment.Y = self.segments[last].Y + start.y
        self.segments.append(segment)

    def adjust_speed(self, dire):
        vel = Point(0, 0)
        last_vel = self.velocity
        if dire[0] > 0: vel.x = 1
        elif dire[0] < 0: vel.x = -1
        elif dire[0] == 0: vel.x = 0
        if dire[1] > 0: vel.y = 1
        elif dire[1] < 0: vel.y = -1
        elif dire[1] == 0: vel.y = 0

        if last_vel.x * vel.x < 0:
            if last_vel.y * vel.y < 0:
                self.velocity = Point(0, -vel.y)
            else:
                self.velocity = Point(0, vel.y)
        elif last_vel.y * vel.x < 0:
            self.velocity = Point(vel.x, 0)
        else:
            self.velocity = vel


def auto_move(snake__):
    food_dir = get_food_direction()

    # set velocity based on direction
    snake__.adjust_speed(food_dir)


class Food(MySprite):
    def __init__(self):
        MySprite.__init__(self)
        image__ = pygame.image.load("hamburger.jpg")
        self.set_image(image__)
        MySprite.update(self, 0, 60)
        self.X = random.randint(0, 100) * 15
        self.Y = random.randint(0, 50) * 15


'''
def get_current_direction():
    global head_x, head_y
    first_segment_x = snake.segments[1].X // 16
    first_segment_y = snake.segments[1].Y // 16
    if head_x-1 == first_segment_x: return 6
    if head_x+1 == first_segment_x: return 4
    if head_y-1 == first_segment_y: return 2
    if head_y+1 == first_segment_y: return 0
'''


def get_food_direction():
    global head_x, head_y
    food__ = Point(0, 0)
    for obj in food_group:
        food__ = Point(obj.X//16, obj.Y//16)
    return food__.x-head_x, food__.y-head_y


screen = game_initialize(100*16, 50*16, "Snake Game", True)
font = pygame.font.SysFont("Arial", 24)
timer = pygame.time.Clock()
game_over = False
auto_mode = False
step_time = 400
last_time = 0

# create a drawing surface
bg_buffer = pygame.Surface((screen.get_rect().width, screen.get_rect().height))

# create snake
snake = Snake()
image = pygame.Surface((60, 60)).convert_alpha()
image.fill((255, 255, 255, 0))
pygame.draw.circle(image, (80, 80, 220, 70), (30, 30), 30, 0)
pygame.draw.circle(image, (80, 80, 250, 255), (30, 30), 30, 4)

# create food
food_group = pygame.sprite.Group()
food = Food()
food_group.add(food)

while True:
    timer.tick(60)
    ticks = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        if auto_mode:
            auto_mode = False
            step_time = 400
        else:
            auto_mode = True
            step_time = 1
    elif keys[K_UP] or keys[K_w]:
        snake.adjust_speed(0)
    elif keys[K_DOWN] or keys[K_s]:
        snake.adjust_speed(2)
    elif keys[K_LEFT] or keys[K_a]:
        snake.adjust_speed(4)
    elif keys[K_RIGHT] or keys[K_d]:
        snake.adjust_speed(6)

    # update section
    if not game_over:
        snake.update(ticks)
        food_group.update(ticks)
        # try to pick up food
        hit_list = pygame.sprite.groupcollide(snake.segments, food_group, False, True)
        if len(hit_list) > 0:
            food_group.add(Food())
            snake.add_segment()

    # see if head collides with body
    for n in range(1, len(snake.segments)):
        if pygame.sprite.collide_rect(snake.segments[0], snake.segments[n]):
            game_over = False

    # check screen boundary
    head_x = snake.segments[0].X // 16
    head_y = snake.segments[0].Y // 16
    if not 0 <= head_x <= 100 or not 0 <= head_y <= 50:
        game_over = False

    # drawing section
    bg_buffer.fill((205, 205, 205))
    snake.draw(bg_buffer)
    food_group.draw(bg_buffer)
    screen.blit(bg_buffer, (0, 0))

    if not game_over:
        if auto_mode:
            auto_move(snake)
        head = snake.segments[0]
        print_text(font, 10, 0, "Length " + str(len(snake.segments)))
        print_text(font, 10, 20, "Position " + str(head.X//16) + "," + str(head.Y//16))
    else:
        print_text(font, 500, 400, "Game Over !")

    pygame.display.update()






















































