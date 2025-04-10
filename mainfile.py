import pygame
import os
import sys
import random
import math
import time
import pytmx as tmx
from spritesheet import Spritesheet
import csv
import json
import tiles
#import pygame_ce

pygame.font.init()

txtfont = pygame.font.SysFont("Arial", 30)

# Do spritesheet for idle animation to maintain player size
"""
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load('monsteridle.png')
    def addzombie(self):
        screen.blit(self.image, (self.x,self.y))
"""

needmoreboolets = []
ourspritesheet = Spritesheet('industrybaby.png')
player_rect = player_img.get_rect()
player_img = ourspritesheet.parse_sprite('gunman000.png')

map = TileMap('industrial_map_ground.csv', spritesheet )
player_rect.x, player_rect.y = map.start_x, map.start_y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, iscreated, x, y, booletvel, stdx, snapshot, isright):
        super().__init__()
        self.iscreated = iscreated
        self.x = x
        self.y = y
        self.booletvel = booletvel
        self.stdx = stdx
        self.snapshot = snapshot
        self.isright = isright
        self.sprites = []
        self.currentsprite = 0
        self.image = 0
    def update(self):
        self.currentsprite += 1

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 21

        self.image = self.sprites[int(self.currentsprite)]
        if self.isright:
            self.image = pygame.transform.flip(self.image, True, False)

        screen.blit(self.image, (self.x,player.y+100))

tsbullet = Bullet(False, 0, 0, 10, 0, False, False)
needmoreboolets.append(tsbullet)

def makeani(tsbullet):

    names = []
    for i in range(22):
        names.append(str(i)+'.png')
    for i in names:
        tsimage = pygame.image.load(i)
        tsimage = pygame.transform.scale(tsimage, (200,200))
        tsbullet.image = tsimage
        tsbullet.sprites.append(tsimage)
    tsbullet.currentsprite = 0
    tsbullet.image = tsbullet.sprites[tsbullet.currentsprite]

    tsbullet.rect = tsbullet.image.get_rect()
    tsbullet.rect.topleft = [tsbullet.x, player.y+100]


class ACRATE(pygame.sprite.Sprite):
    def __init__(self, numbullets, isshowing, x):
        super().__init__()
        self.numbullets = numbullets
        self.img = pygame.image.load('ammocrate.png')
        self.img = pygame.transform.scale(self.img, (100,75))
        self.rect = self.img.get_rect()
        self.rect.topleft = [x-100,225]
        self.isshowing = isshowing
        self.x = x

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.goingright = False
        self.sprites = []
        self.jumpsprites = []
        self.currentjumpsprite = 0
        self.idlesprites = []
        self.currentidlesprite = 0
        self.hurtsprites = []
        self.currenthurtsprite = 0
        self.cooldowncount = 0
        self.ispunching = False
        self.currentdiesprite = 0
        self.diesprites = []
        self.currentgunsprite = 0
        self.gunsprites = []
        self.ratio = 1
    def cooldown(self):
        """
        if self.cooldowncount == 10:
            self.cooldowncount = 0
        elif self.cooldowncount >= 0:
            self.cooldowncount += 1
        """
    def gunman(self):
        self.cooldown()
        if self.cooldowncount == 0:
            self.image = self.gunsprites[int(self.currentgunsprite)]
            if self.goingright:
                self.image = pygame.transform.flip(self.image, True, False)
            self.currentgunsprite += 0.2
            if self.currentgunsprite >= len(self.gunsprites):
                self.ispunching = False
                self.currentgunsprite = 0
            if round(self.currentgunsprite, 1) == 3.0:
                tsbullet = Bullet(True, 0, 0, 10, 0, False, False)
                needmoreboolets.append(tsbullet)
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
        self.currentidlesprite += 0.2

        if self.currentidlesprite >= len(self.idlesprites):
            self.currentidlesprite = 0

        self.image = self.idlesprites[int(self.currentidlesprite)]
        if self.goingright:
            self.image = pygame.transform.flip(self.image, True, False)
    def punch(self):
        self.cooldown()
        if self.cooldowncount == 0:
            self.image = self.hurtsprites[int(self.currenthurtsprite)]
            if self.goingright:
                self.image = pygame.transform.flip(self.image, True, False)
            self.currenthurtsprite += 0.3
            if self.currenthurtsprite >= len(self.hurtsprites):
                self.ispunching = False
                self.currenthurtsprite = 0
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
    def die(self):

        running = True

        self.currentdiesprite += 0.1
        self.ratio -= 0.025

        if self.currentdiesprite >= len(self.diesprites):
            running = False
            self.currentdiesprite = 0

        self.image = self.diesprites[int(self.currentdiesprite)]
        if self.goingright:
            self.image = pygame.transform.flip(self.image, True, False)
        
        return running

class boolets:
    def __init__(self, bullets, text, font, textcol, x, y):
        self.bullets = bullets
        self.text = text
        self.font = font
        self.textcol = textcol
        self.x = x
        self.y = y
    def drawtxt(self):
        img = self.font.render(self.text+str(self.bullets), True, self.textcol)
        screen.blit(img, (self.x,self.y))


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

x = 100
y = 100

bullets = boolets(0, "Bullets: ", txtfont, (255,255,255), 0, 570)

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

#monster = Monster(0, random.randrange(0,SCREEN_HEIGHT-20), 25)

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

ispunching = False

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

idlenames = []
for i in range(4):
    idlenames.append('idle00'+str(i)+'.png')
for i in idlenames:
    tsimage = pygame.image.load(i)
    tsimage = pygame.transform.scale(tsimage, (200,200))
    player.image = tsimage
    player.idlesprites.append(tsimage)
player.currentidlesprite = 0
player.image = player.idlesprites[player.currentidlesprite]

player.rect = player.image.get_rect()
player.rect.topleft = [player.x, player.y]

hurtnames = []
for i in range(6):
    hurtnames.append('hurt00'+str(i)+'.png')
for i in hurtnames:
    tsimage = pygame.image.load(i)
    tsimage = pygame.transform.scale(tsimage, (200,200))
    player.image = tsimage
    player.hurtsprites.append(tsimage)
player.currenthurtsprite = 0
player.image = player.hurtsprites[player.currenthurtsprite]

player.rect = player.image.get_rect()
player.rect.topleft = [player.x, player.y]

dienames = []
for i in range(6):
    dienames.append('die00'+str(i)+'.png')
for i in dienames:
    tsimage = pygame.image.load(i)
    tsimage = pygame.transform.scale(tsimage, (200,200))
    player.image = tsimage
    player.diesprites.append(tsimage)
player.currentdiesprite = 0
player.image = player.diesprites[player.currentdiesprite]

player.rect = player.image.get_rect()
player.rect.topleft = [player.x, player.y]

gunnames = []
for i in range(6):
    gunnames.append('coolio00'+str(i)+'.png')
for i in gunnames:
    tsimage = pygame.image.load(i)
    tsimage = pygame.transform.scale(tsimage, (200,200))
    player.image = tsimage
    player.gunsprites.append(tsimage)
player.currentgunsprite = 0
player.image = player.gunsprites[player.currentgunsprite]

player.rect = player.image.get_rect()
player.rect.topleft = [player.x, player.y]

timerevent = pygame.event.custom_type()
pygame.time.set_timer(timerevent, 1000)

last = pygame.time.get_ticks()
now = pygame.time.get_ticks()

isdying = False

player.ratio=1

tscrate = ACRATE(5, True, 300)

#booletvel = 10

while running:

    screen.fill((0,0,0))

    #print(needmoreboolets)

    for i in needmoreboolets:

        if i.snapshot == False:
            makeani(i)
            i.snapshot = True
            if player.goingright:
                i.stdx = player.x+150
            else:
                i.stdx = player.x
            i.isright = player.goingright
            i.x = i.stdx

        if i.x >= SCREEN_WIDTH or i.x <= -100:
            i.iscreated = False
            #i.x = 0
            i.booletvel = 1
            #i.iscreated = False
            needmoreboolets.remove(i)

        if i.iscreated == True:
            i.update()
            #screen.blit(i.image, (i.x, 150))
            if not(i.isright):
                i.x += i.booletvel
                #pygame.draw.circle(screen, "pink", (i.x, player.y+100), 20)
                #i.booletvel += 1
            else:
                i.x -= i.booletvel
                #pygame.draw.circle(screen, "pink", (i.x, player.y+100), 20)
                #i.booletvel += 1

    if tscrate.isshowing:
        screen.blit(tscrate.img, (tscrate.x,225))
    else:
        tscrate = ACRATE(5, True, random.randrange(100, 700, 5))

    if player.x == tscrate.rect.topleft[0]:
        print("Touching")
        bullets.bullets += tscrate.numbullets
        tscrate.isshowing = False
        #tscrate.x = -500000
        #tscrate.rect.topleft = [tscrate.x, 150]

    bullets.drawtxt()

    pygame.draw.rect(screen, "red", (0,0,300,40))
    pygame.draw.rect(screen, "green", (0,0,300*player.ratio,40))

    #monster.addzombie()
    #monster.x += monster.speed

    key = pygame.key.get_pressed()
    screen.blit(player.image, (player.x, player.y))
    #movingsprites.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_b]:
        bullets.bullets += 1
    if keys[pygame.K_d]:
        isdying = True
    if keys[pygame.K_x]:
        if bullets.bullets == 0:
            print("No bullets.")
        else:
            if now-last > 1500:
                last = pygame.time.get_ticks()
                bullets.bullets -= 1
                player.ispunching = True
    if keys[pygame.K_SPACE]:
        isjumping = True
        #player.jumpdate()
    if keys[pygame.K_LEFT]:
        player.update()
        player.goingright = True
        #screen.fill((0,0,0))
        #player.update()
        #player.image = pygame.transform.flip(player.image, True, False)
        #movingsprites = pygame.sprite.Group()
        #movingsprites.add(player)
        #screen.blit(player.image, (player.x, player.y))
        player.changex(-5)
    elif keys[pygame.K_RIGHT]:
        player.update()
        player.goingright = False
        player.changex(5)
    else:
        player.idling()

    if isjumping:
        #screen.fill((0,0,0))
        player.jumpdate()
        player.y -= y_vel
        y_vel -= y_gravity
        if y_vel < -jump_height:
            isjumping = False
            y_vel = jump_height
    if player.ispunching:
        player.gunman()
        #pygame.draw.circle(screen, "pink", (player.x+125,player.y+125), 20)
    if isdying:
        tssssss = player.die()
        if not(tssssss):
            running = False

    if player.x >= SCREEN_WIDTH-100:
        player.x = SCREEN_WIDTH-100
        player.rect.topleft = [player.x, player.y]
    if player.x <= -100:
        player.x = -100
        player.rect.topleft = [player.x, player.y]

    pygame.display.flip()
    clock.tick(30)

    now = pygame.time.get_ticks()

pygame.quit()