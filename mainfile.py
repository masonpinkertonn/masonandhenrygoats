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

player = pygame.image.load('soldier.png')
width = player.get_rect().width
height = player.get_rect().height

running = True
x = 0
y = 0
clock = pygame.time.Clock()

delta_time = 0.1

while running:

    screen.fill((0,0,0))

    player = pygame.transform.scale(player, (width, height))

    screen.blit(player, (x, y))

    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= 1
    elif keys[pygame.K_RIGHT]:
        x += 1
    elif keys[pygame.K_UP]:
        y -= 1
    elif keys[pygame.K_DOWN]:
        y += 1

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()