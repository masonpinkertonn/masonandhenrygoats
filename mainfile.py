import pygame
import os
import sys
import random
import math
import time

# Do spritesheet for idle animation to maintain player size

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.goingright = False
        self.sprites = []
        self.jumpsprites = []
        self.currentjumpsprite = 0
    def update(self):
        self.currentsprite += 0.2

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0

        self.image = self.sprites[int(self.currentsprite)]
        if self.goingright:
            self.image = pygame.transform.flip(self.image, True, False)
    def jumpdate(self):
        self.currentjumpsprite += 0.2

        if self.currentjumpsprite >= len(self.jumpsprites):
            self.currentjumpsprite = 0

        self.image = self.jumpsprites[int(self.currentjumpsprite)]
        if self.goingright:
            self.image = pygame.transform.flip(self.image, True, False)
    def idling(self):
        tsimage = pygame.image.load('Biker_idle.png')
        tsimage = pygame.transform.scale(tsimage, (200,200))
        player.image = tsimage
        player.rect = player.image.get_rect()
        player.rect.topleft = [player.x, player.y]
    def changex(self, xval):
        self.x+=xval
        self.rect.topleft = [self.x, self.y]
    def changey(self, isjumping):
        self.y -= y_vel
        y_vel -= y_gravity
        if y_vel < -jump_height:
            isjumping = False
            y_vel = jump_height
        return isjumping


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

isjumping = True

y_gravity = 1
jump_height = 20
y_vel = jump_height

movingsprites = pygame.sprite.Group()
player = Player(x,y)
movingsprites.add(player)

isrunning = True

names = []
for i in range(6):
    names.append('tile00'+str(i)+'.png')
for i in names:
    tsimage = pygame.image.load(i)
    tsimage = pygame.transform.scale(tsimage, (200,200))
    player.image = tsimage
    player.sprites.append(tsimage)
player.currentsprite = 0
player.image = player.sprites[player.currentsprite]

player.rect = player.image.get_rect()
player.rect.topleft = [player.x, player.y]



jumpnames = []
for i in range(4):
    jumpnames.append('jump00'+str(i)+'.png')
for i in jumpnames:
    tsimage = pygame.image.load(i)
    tsimage = pygame.transform.scale(tsimage, (200,200))
    player.image = tsimage
    player.jumpsprites.append(tsimage)
player.currentjumpsprite = 0
player.image = player.jumpsprites[player.currentjumpsprite]

player.rect = player.image.get_rect()
player.rect.topleft = [player.x, player.y]

while running:

    screen.fill((0,0,0))

    key = pygame.key.get_pressed()
    screen.blit(player.image, (player.x, player.y))
    #movingsprites.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.update()
        player.goingright = True
        #screen.fill((0,0,0))
        #player.update()
        #player.image = pygame.transform.flip(player.image, True, False)
        #movingsprites = pygame.sprite.Group()
        #movingsprites.add(player)
        #screen.blit(player.image, (player.x, player.y))
        player.changex(-2)
    elif keys[pygame.K_RIGHT]:
        player.update()
        player.goingright = False
        player.changex(2)
    elif keys[pygame.K_SPACE]:
        isjumping = True
        player.jumpdate()
    else:
        player.idling()

    if isjumping:
        #screen.fill((0,0,0))
        player.y -= y_vel
        y_vel -= y_gravity
        if y_vel < -jump_height:
            isjumping = False
            y_vel = jump_height


    pygame.display.flip()
    clock.tick(30)

pygame.quit()