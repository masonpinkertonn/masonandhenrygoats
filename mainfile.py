import pygame
import os
import sys
import random
import math
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.goingright = False
        self.sprites = []
        names = []
        for i in range(6):
            names.append('tile00'+str(i)+'.png')
        for i in names:
            tsimage = pygame.image.load(i)
            tsimage = pygame.transform.scale(tsimage, (200,200))
            self.image = tsimage
            self.sprites.append(tsimage)
        self.currentsprite = 0
        self.image = self.sprites[self.currentsprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
    def update(self):
        self.currentsprite += 0.2

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0

        self.image = self.sprites[int(self.currentsprite)]
        if self.goingright:
            self.image = pygame.transform.flip(self.image, True, False)
    def changex(self, xval):
        self.x+=xval
        self.rect.topleft = [self.x, self.y]


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

x = 100
y = 100

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
player = Player(x,y)
movingsprites.add(player)

while running:

    screen.fill((0,0,0))

    key = pygame.key.get_pressed()
    screen.blit(player.image, (player.x, player.y))
    #movingsprites.draw(screen)
    
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.goingright = True
        #screen.fill((0,0,0))
        #player.update()
        #player.image = pygame.transform.flip(player.image, True, False)
        #movingsprites = pygame.sprite.Group()
        #movingsprites.add(player)
        #screen.blit(player.image, (player.x, player.y))
        player.changex(-2)
    elif keys[pygame.K_RIGHT]:
        player.goingright = False
        player.changex(2)
    elif keys[pygame.K_SPACE]:
        isjumping = True

    if isjumping:
        screen.fill((0,0,0))
        player.y -= y_vel
        y_vel -= y_gravity
        if y_vel < -jump_height:
            isjumping = False
            y_vel = jump_height


    pygame.display.flip()
    clock.tick(30)

pygame.quit()