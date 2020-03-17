import sys
import time
import random
import math
import pygame

import Function_Set
from Function_Set import *

global screen, font, timer, level, levels
global paddle_group, block_group, ball_group
global paddle, block_image, block, ball


def game_init(screen_width, screen_height, caption, mouse_visible=False):
    global screen, font, timer
    global paddle_group, block_group, ball_group
    global paddle, block_image, block, ball

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(caption)
    font = pygame.font.SysFont("Arial", 24)
    pygame.mouse.set_visible(mouse_visible)
    timer = pygame.time.Clock()

    # create sprite groups
    paddle_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    ball_group = pygame.sprite.Group()

    # create the paddle sprite
    paddle = MySprite()
    paddle.load("paddle.png")
    paddle.position = 400, 540
    paddle_group.add(paddle)

    # create the ball sprite
    ball = MySprite()
    ball.load("ball.png")
    ball.position = 400, 500
    ball_group.add(ball)


def reset_levels():
    global level, levels
    levels = []
    for le in range(level+1):
        levels.append([])
        for new_block in range((level + 1) * 12):
            levels[le].append(random.choice([0, 1]))


# this function increments the level
def goto_next_level():
    global level, levels
    level += 1
    reset_levels()
    load_level()


# this function updates the blocks in play
def update_blocks():
    global block_group, waiting
    if len(block_group) == 0:
        # all blocks gone?
        goto_next_level()
        waiting = True
    block_group.update(ticks, 50)


# this function sets up the blocks for the level
def load_level():
    global level, levels, block_image, block_group, block
    block_image = pygame.image.load("blocks.png").convert_alpha()
    block_group.empty() # reset block group
    for bx in range(0, 12):
        for by in range(level + 1):
            block = MySprite()
            block.set_image(block_image, 58, 28, 4)
            x = 40 + bx * (block.frame_width + 1)
            y = 60 + by * (block.frame_height + 1)
            block.position = x, y
            # read blocks from level data
            num = levels[by][bx]
            block.first_frame = level
            block.last_frame = level
            if num: block_group.add(block)


# this function moves the paddle
def move_paddle():
    global move_x, move_y, keys, waiting, game_start
    paddle_group.update(ticks, 50)
    if keys[K_SPACE]:
        game_start = True
        if waiting:
            waiting = False
            reset_ball()
    elif keys[K_LEFT]: paddle.velocity.x = -10.0
    elif keys[K_RIGHT]: paddle.velocity.x = 10.0
    else:
        if move_x < -2: paddle.velocity.x = move_x
        elif move_x > 2: paddle.velocity.x = move_x
        else: paddle.velocity.x = 0
    paddle.X += paddle.velocity.x
    if paddle.X < 0: paddle.X = 0
    elif paddle.X > 710: paddle.X = 710


# this function resets the ball's velocity
def reset_ball():
    ball.velocity = Point(random.choice([5, -5]), -10)


# this function moves the ball
def move_ball():
    global waiting, ball, game_over, lives
    # move the ball
    ball_group.update(ticks, 50)
    if waiting:
        ball.X = paddle.X + 40
        ball.Y = paddle.Y - 20
    ball.X += ball.velocity.x
    ball.Y += ball.velocity.y
    if ball.X < 0:
        ball.X = 0
        ball.velocity.x *= -1
    elif ball.X > 780:
        ball.X = 780
        ball.velocity.x *= -1
    if ball.Y < 0:
        ball.Y = 0
        ball.velocity.y *= -1
    elif ball.Y > 580: # missed paddle
        # ball.velocity.y *= -1
        waiting = True
        lives -= 1
        if lives < 1:
            game_over = True


# this function test for collision between ball and paddle
def collision_ball_paddle():
    if pygame.sprite.collide_rect(ball, paddle):
        ball.velocity.y = -abs(ball.velocity.y)
        bx = ball.X + 8
        # by = ball.Y + 8
        px = paddle.X + paddle.frame_width / 2
        # py = paddle.Y + paddle.frame_height / 2
        if bx < px: # left side of paddle
            ball.velocity.x = -abs(ball.velocity.x + random.randint(-4, 4))
        else:
            ball.velocity.x = abs(ball.velocity.x + random.randint(-4, 4))


# this function tests for collision between ball and blocks
def collision_ball_blocks():
    global score, block_group, ball

    hit_block = pygame.sprite.spritecollideany(ball, block_group)
    if hit_block:
        score += 10
        block_group.remove(hit_block)
        bx = ball.X + 8
        by = ball.Y + 8
        # hit middle of block from above or below
        if hit_block.X+5 < bx < hit_block.X + hit_block.frame_width-5:
            if by < hit_block.Y + hit_block.frame_height/2:
                ball.velocity.y = -abs(ball.velocity.y)
            else:
                ball.velocity.y = abs(ball.velocity.y)
        elif bx < hit_block.X+5:
            ball.velocity.x = -abs(ball.velocity.x)
        elif bx > hit_block.X + hit_block.frame_width-5:
            ball.velocity.x = abs(ball.velocity.x)
        else:
            ball.velocity.y *= -1


# this function draw all print text
def draw_text():
    print_text(font, 0, 0, "Score: " + str(score))
    print_text(font, 200, 0, "Level: " + str(level+1))
    print_text(font, 400, 0, "Blocks: " + str(len(block_group)))
    print_text(font, 670, 0, "Balls: " + str(lives))
    print_text(font, 0, 30, "Ball's velocity: X  " + str(ball.velocity.x) + "  Y  " + str(ball.velocity.y))
    if (not game_start) and lives == 5:
        print_text(font, 200, 500, "Press Mouse / Space To Start Game")
    if game_over:
        print_text(font, 300, 380, "G A M E O V E R")


# main program begins
game_init(800, 600, "Block Breaker Game", True)
game_start = False
game_over = False
waiting = True
score = 0
lives = 5
level = 0

reset_levels()
load_level()
bg_red, bg_green, bg_blue = random.randint(10, 240), random.randint(10, 240), random.randint(10, 240)
# repeating loop
while True:
    timer.tick(60)
    ticks = pygame.time.get_ticks()

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEMOTION:
            move_x, move_y = event.rel
        elif event.type == MOUSEBUTTONUP:
            game_start = True
            if waiting:
                waiting = False
                reset_ball()
            elif event.type == KEYUP:
                if event.key == K_RETURN:
                    goto_next_level()

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()

    # do updates
    if not game_over:
        update_blocks()
        move_paddle()
        move_ball()
        collision_ball_paddle()
        collision_ball_blocks()

    # do drawing
    if bg_red >= 240:
        bg_red = random.randint(10, 150)
    else:
        bg_red += 0.05
    if bg_green >= 240:
        bg_green = random.randint(10, 150)
    else:
        bg_green += 0.05
    if bg_blue >= 240:
        bg_blue = random.randint(10, 150)
    else:
        bg_blue += 0.05
    screen.fill((int(bg_red), int(bg_green), int(bg_blue)))
    block_group.draw(screen)
    ball_group.draw(screen)
    paddle_group.draw(screen)
    draw_text()
    pygame.display.update()
