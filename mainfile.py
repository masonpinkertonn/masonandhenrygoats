import pygame
import os
import sys
import random
import math
import time

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.image.load('Biker_idle.png')
width = player.get_rect().width
width *= 2
height = player.get_rect().height
height *= 2

playerjump = pygame.image.load('Biker_jump.png')
jumpwidth = playerjump.get_rect().width
jumpwidth *= 2
jumpheight = playerjump.get_rect().height
jumpheight *= 2

running = True
x = 0
y = 255
clock = pygame.time.Clock()

isjumping = False

y_gravity = 1
jump_height = 20
y_vel = jump_height

delta_time = 0.1

while running:

    screen.fill((0,0,0))

    player = pygame.transform.scale(player, (width, height))
    playerjump = pygame.transform.scale(playerjump, (jumpwidth, jumpheight))

    screen.blit(player, (x, y))

    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        screen.fill((0,0,0))
        screen.blit(pygame.transform.flip(player, True, False), (x, y))
        x -= 1
    elif keys[pygame.K_RIGHT]:
        x += 1
    elif keys[pygame.K_SPACE]:
        isjumping = True

    if isjumping:
        screen.fill((0,0,0))
        screen.blit(playerjump, (x, y))
        y -= y_vel
        y_vel -= y_gravity
        if y_vel < -jump_height:
            isjumping = False
            y_vel = jump_height

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()