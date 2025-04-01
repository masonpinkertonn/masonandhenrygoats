import pygame
import os
import sys
import random
import math
import time

def thememusic():
    pygame.mixer.init()
    pygame.mixer.music.load('thick_of_it_by_ksi.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(7000)

pygame.init()
thememusic()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.image.load('yur.webp')
width = player.get_rect().width
height = player.get_rect().height

running = True
x = 0
clock = pygame.time.Clock()

delta_time = 0.1

while running:

    screen.fill((0,0,0))

    player = pygame.transform.scale(player, (width/20, height/20))

    screen.blit(player, (x, 250))

    x += 1

    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                location -= 1

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()