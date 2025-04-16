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
from tiles import *
import tralalalero_tralala as tralalalerotralala
#import pygame_ce

pygame.font.init()

bg = pygame.image.load('peakbkg.jpg')
bg = pygame.transform.scale(bg, (1920, 1080))
pygame.mouse.set_visible(0)


txtfont = pygame.font.SysFont("Arial", 30)
pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
player_img = ourspritesheet.parse_sprite('Biker_idle.png')
player_rect = player_img.get_rect()

map = Tilemap('industrial_map_ground.csv', ourspritesheet)
player_rect.x, player_rect.y = map.start_x, map.start_y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, iscreated, x, y, booletvel, stdx, stdy, snapshot, isright):
        super().__init__()
        self.iscreated = iscreated
        #self.x = x
        #self.y = y
        self.booletvel = booletvel
        self.stdx = stdx
        self.snapshot = snapshot
        self.isright = isright
        self.sprites = []
        self.currentsprite = 0
        self.image = pygame.image.load("LeMonke.webp")
        self.rect = self.image.get_rect()
        self.stdy = stdy
    def update(self):
        self.currentsprite += 1

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 21

        self.image = self.sprites[int(self.currentsprite)]
        if self.isright:
            self.image = pygame.transform.flip(self.image, True, False)

        screen.blit(self.image, (self.rect.x,self.rect.y))

    def checks(self):
        if self.snapshot == False:
            makeani(self)
            self.snapshot = True
            self.stdy = player.rect.y + 25
            if player.goingright:
                self.stdx = player.rect.x+50
            else:
                self.stdx = player.rect.x
            self.isright = player.goingright
            self.rect.x = self.stdx
            self.rect.y = self.stdy

        if self.rect.x >= SCREEN_WIDTH or self.rect.x <= -100:
            self.iscreated = False
            #i.x = 0
            self.booletvel = 1
            #i.iscreated = False
            needmoreboolets.remove(self)

        if self.iscreated == True:
            self.update()
            #screen.blit(i.image, (i.x, 150))
            if not(self.isright):
                self.rect.x += self.booletvel
                #pygame.draw.circle(screen, "pink", (i.x, player.rect.y+100), 20)
                #i.booletvel += 1
            else:
                self.rect.x -= self.booletvel
                #pygame.draw.circle(screen, "pink", (i.x, player.rect.y+100), 20)
                #i.booletvel += 1

tsbullet = Bullet(False, 0, 0, 10, 0, 0, False, False)
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
    #tsbullet.rect.topleft = [tsbullet.x, player.rect.y+25]


class ACRATE(pygame.sprite.Sprite):
    def __init__(self, numbullets, isshowing, x):
        super().__init__()
        self.numbullets = numbullets
        self.img = pygame.image.load('ammocrate.png')
        #self.img = pygame.transform.scale(self.img, (100,75))
        self.rect = self.img.get_rect()
        self.rect.x = x
        #self.rect.topleft = [x-100,225]
        self.isshowing = isshowing
        #self.x = x

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.x = x
        #self.y = y
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
        self.image = pygame.image.load('coolio000.png')
        self.rect=self.image.get_rect()
        self.isjumping = False
        self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.accel = pygame.math.Vector2(0,0.35)
        self.onground = False
        self.tempvel = 0
        self.isposvel = 0
        self.y_gravity = 1
        self.jump_height = 20
        self.y_vel = self.jump_height
        #self.hitbox = pygame.Rect(player.rect.x, player.rect.y)
        #self.position.x = map.start_x
        #self.position.y = map.start_y
    #def checkstuff(self, tiles):
        #self.
    def gethits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits
    def checkCollisionsx(self, tiles):
        collisions = self.gethits(tiles)
        for tile in collisions:
            dr = abs(self.rect.right - tile.rect.left)
            dl = abs(self.rect.left - tile.rect.right)
            db = abs(self.rect.bottom - tile.rect.top)
            dt = abs(self.rect.top - tile.rect.bottom)
            collision_side = ""
            min_dist = min(dr, dl, db, dt)

            if min_dist == dr:
                collision_side = "right"
            elif min_dist == dl:
                collision_side = "left"

            if collision_side == "right":
                self.rect.x = tile.rect.left - self.rect.w
            elif collision_side == "left":
                self.rect.x = tile.rect.right
    def checkCollisionsy(self, tiles):
        self.onground = False
        self.tempvel += 1
        self.rect.bottom += self.tempvel
        collisions = self.gethits(tiles)
        for tile in collisions:
            self.tempvel = 0
            self.rect.bottom = tile.rect.bottom-30#self.rect.h
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
                tsbullet = Bullet(False, 0, 0, 10, 0, 0, False, False)
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
        if xval < 0:
            self.isposvel = -1
        elif xval > 0:
            self.isposvel = 1
        else:
            self.isposvel = 0
        self.rect.x+=xval
        print(self.isposvel)
        #self.rect.topleft = [self.rect.x, self.y]
    def changey(self, tiles):
        self.rect.y -= self.y_vel
        self.y_vel -= self.y_gravity
        collisions = self.gethits(tiles)
        for tile in collisions:
            dr = abs(self.rect.right - tile.rect.left)
            dl = abs(self.rect.left - tile.rect.right)
            db = abs(self.rect.bottom - tile.rect.top)
            dt = abs(self.rect.top - tile.rect.bottom)
            collision_side = ""
            min_dist = min(dr, dl, db, dt)

            if min_dist == dr:
                collision_side = "right"
            elif min_dist == dl:
                collision_side = "left"
            elif min_dist == dt:
                collision_side = "top"
            if collision_side == "top":
                self.isjumping = False
                self.y_vel = self.jump_height
                self.onground = False
        
        return self.isjumping
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
#player.rect.topleft = [player.rect.x, player.rect.y]



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
#player.rect.topleft = [player.rect.x, player.rect.y]

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
#player.rect.topleft = [player.rect.x, player.rect.y]

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
#player.rect.topleft = [player.rect.x, player.rect.y]

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
#player.rect.topleft = [player.rect.x, player.rect.y]

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
#player.rect.topleft = [player.rect.x, player.rect.y]

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
player.rect.y += 100
#player.rect.topleft = [player.rect.x, player.rect.y]

timerevent = pygame.event.custom_type()
pygame.time.set_timer(timerevent, 1000)

last = pygame.time.get_ticks()
now = pygame.time.get_ticks()

isdying = False

player.ratio=1

tscrate = ACRATE(5, True, 300)

#booletvel = 10
"""
player.rect.w -= 60
player.rect.y = 50
player.rect.height -= 50
"""
print(player.rect.w)
print(player.rect.h)
tscrate.rect.y+=150
player.rect = player.rect.inflate((-168,-168))

while running:
    
    screen.fill((0,0,0))
    screen.blit(bg, (0, 0))

    player.image = pygame.transform.scale(player.image,(32,32))

    player.checkCollisionsx(map.tiles)
    #player.checkCollisionsy(map.tiles)

    player.isposvel = 0

    r1 = pygame.draw.rect(screen, "red", (player.rect.x,player.rect.y,player.rect.w,player.rect.h))
    r2 = pygame.draw.rect(screen, "blue", (tscrate.rect.x,tscrate.rect.y,tscrate.rect.w,tscrate.rect.h))
    map.draw_map(screen)

    #print(needmoreboolets)

    if len(needmoreboolets) > 1:
        print("ok")

        needmoreboolets[1].checks()

    if tscrate.isshowing:
        screen.blit(tscrate.img, (tscrate.rect.x,tscrate.rect.y))
    else:
        tscrate = ACRATE(5, True, random.randrange(100, 700, 5))
        tscrate.rect.y+=150

    if r1.colliderect(r2):
        print("goat")

    if player.rect.colliderect(tscrate.rect):
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
    screen.blit(player.image, (player.rect.x, player.rect.y))
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
        print("hola")
        if not(needmoreboolets[-1].iscreated):
            if bullets.bullets == 0:
                print("No bullets.")
            else:
                if now-last > 1500:
                    last = pygame.time.get_ticks()
                    bullets.bullets -= 1
                    player.ispunching = True
    if keys[pygame.K_SPACE]:
        player.isjumping = True
        #player.jumpdate()
    if keys[pygame.K_LEFT]:
        player.update()
        player.goingright = True
        #screen.fill((0,0,0))
        #player.update()
        #player.image = pygame.transform.flip(player.image, True, False)
        #movingsprites = pygame.sprite.Group()
        #movingsprites.add(player)
        #screen.blit(player.image, (player.rect.x, player.rect.y))
        player.changex(-5)
    elif keys[pygame.K_RIGHT]:
        player.update()
        player.goingright = False
        player.changex(5)
    else:
        player.idling()

    if player.isjumping:
        #screen.fill((0,0,0))
        player.jumpdate()
        player.changey(map.tiles)
    if player.ispunching:
        player.gunman()
        #pygame.draw.circle(screen, "pink", (player.rect.x+125,player.rect.y+125), 20)
    if isdying:
        tssssss = player.die()
        if not(tssssss):
            running = False

    if player.rect.x >= SCREEN_WIDTH-100:
        player.rect.x = SCREEN_WIDTH-100
        #player.rect.topleft = [player.rect.x, player.rect.y]
    if player.rect.x <= -100:
        player.rect.x = -100
        #player.rect.topleft = [player.rect.x, player.rect.y]

    pygame.display.flip()
    clock.tick(30)

    now = pygame.time.get_ticks()

pygame.quit()