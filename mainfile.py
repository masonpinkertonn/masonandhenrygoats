import pygame
import os
import sys
import random
import math
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('tile000.png'))
        self.sprites.append(pygame.image.load('tile001.png'))
        self.sprites.append(pygame.image.load('tile002.png'))
        self.sprites.append(pygame.image.load('tile003.png'))
        self.sprites.append(pygame.image.load('tile004.png'))
        self.sprites.append(pygame.image.load('tile005.png'))
        self.currentsprite = 0
        self.image = self.sprites[self.currentsprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
    def update(self):
        self.currentsprite += 0.2

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0

        self.image = self.sprites[int(self.currentsprite)]


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

x = 0
y = 255

"""
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
"""

running = True
clock = pygame.time.Clock()

isjumping = False

y_gravity = 1
jump_height = 20
y_vel = jump_height

movingsprites = pygame.sprite.Group()
player = Player(10,10)
movingsprites.add(player)

while running:

    screen.fill((0,0,0))

    """

    player = pygame.transform.scale(player, (width, height))
    playerjump = pygame.transform.scale(playerjump, (jumpwidth, jumpheight))
    screen.blit(player, (x, y))

    key = pygame.key.get_pressed()
    """
    movingsprites.draw(screen)
    movingsprites.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    """
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
    """

    pygame.display.flip()
    clock.tick(60)

pygame.quit()