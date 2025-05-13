import pygame
import random
import textwrap
from pytmx import *
from pygame_aseprite_animation import *
from pytmx.util_pygame import load_pygame
from top_down_sprites import *
from Camera2 import *
import time
pygame.init()
pygame.font.init()
pygame.mixer.init()
image_cache={}
inshop = {"Pie": ["Pie",5,1], "Cake":["Cake",10,2], "Super Health Potion":["Super Health Potion",15,3]}
# Preload music for each gamestate
music_files = {
    "main": "Balatro - Complete Original Soundtrack (Official).mp3",
    "fight": "Doom Eternal OST - The Only Thing They Fear Is You (Mick Gordon) [Doom Eternal Theme].mp3",
    "gameover": "gameover.mp3",
}
current_music = None
wrapper = textwrap.TextWrapper(width=30)


cols = ["black", "green", "blue", "yellow", "orange", "pink", "purple"]



sound_effects_channel = pygame.mixer.Channel(1)
vine_boom_sound = pygame.mixer.Sound("vine-boom.mp3")
vine_boom_sound.set_volume(1.0)  
metal_pipe_sound = pygame.mixer.Sound("metalpipe.mp3")
metal_pipe_sound.set_volume(1.0)  
compinf = pygame.display.Info()

SCREEN_WIDTH =  compinf.current_w #1280
SCREEN_HEIGHT = compinf.current_h #720

wrapwidth = 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
tmx_data = load_pygame('map/smallmap.tmx')

cameraX = 0
cameraY = 0
def load_image(filename, scale=None):
    if filename not in image_cache:
        #print(f"Loading image: {filename}")
        image = pygame.image.load(filename)
        if scale:
            image = pygame.transform.scale(image, scale)
        image_cache[filename] = image
    return image_cache[filename]

for layer in tmx_data.layers:
    if hasattr (layer, 'data'):
        #print(layer)
        for x,y,surf in layer.tiles():
            pos = (x * tmx_data.tilewidth, y * tmx_data.tileheight)
            Tile(pos = pos, surf = surf, groups = sprite_group)

for obj in tmx_data.objects:
    pos = (obj.x, obj.y)
    if obj.image:
        Tile(pos = pos, surf = obj.image, groups = sprite_group)


class hitbutton:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
gameover = pygame.image.load('gameover.png')
wingame = pygame.image.load('wingame.png')
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 20
        self.isgolemdefeated = False
        self.isbirddefeated = False
        self.isplantdefeated = False
        self.iswizdefeated = False
        self.goingup = False
        self.goingdown = False
        self.goingleft = False
        self.goingright = False
        self.sprites = []
        names = []
        for i in range(10):
            names.append('Wraith_01_Idle_00'+str(i)+'.png')
        names.append('Wraith_01_Idle_010.png')
        names.append('Wraith_01_Idle_011.png')
        for i in names:
            tempimg = pygame.image.load(i)
            tempimg = pygame.transform.scale(tempimg, (100.5,144.5))
            self.sprites.append(tempimg)
        self.currentsprite = 0
        self.movesprites = []
        movenames = []
        for i in range(10):
            movenames.append('Wraith_01_Moving Forward_00'+str(i)+'.png')
        movenames.append('Wraith_01_Moving Forward_010.png')
        movenames.append('Wraith_01_Moving Forward_011.png')
        for i in movenames:
            tempimg = pygame.image.load(i)
            tempimg = pygame.transform.scale(tempimg, (100.5,144.5))
            self.movesprites.append(tempimg)
        self.currentmovesprite = 0
        self.image = self.sprites[self.currentsprite]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH/3
        self.rect.y = SCREEN_HEIGHT/3
        self.isleft = False
        self.ismoving = False
    def docollisions(self, rct):
        if self.goingleft:
            self.rect.left = rct.right#-1
        if self.goingdown:
            self.rect.bottom = rct.top#+1
        if self.goingup:
            self.rect.top = rct.bottom#-1
        if self.goingright:
            self.rect.right = rct.left#+1
    def idleanimation(self):
        self.currentsprite += 0.2

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0

        self.image = self.sprites[int(self.currentsprite)]

        if self.isleft:
            self.image = pygame.transform.flip(self.image, True, False)
    def movement(self):

        self.ismoving = True

        self.currentmovesprite += 0.2

        if self.currentmovesprite >= len(self.movesprites):
            self.currentmovesprite = 0

        self.image = self.movesprites[int(self.currentmovesprite)]

        if self.isleft:
            self.image = pygame.transform.flip(self.image, True, False)

birb = Bird()

planto = PSHOOTER()

thiswiz = Wizard()

thiswiz.rect.x = 500

def golemdialogue(currentline, fname):
    dialogue = open(fname, 'r')
    lines = []
    for line in dialogue:
        if '\n' in line:
            line = line[0:-1]
        mytxt = wrapper.wrap(line)
        if len(mytxt) > 1:
            lines.append(mytxt)
        elif len(mytxt) == 1:
            lines.append(mytxt[0])
    dialogue.close()
    while True:
        try:
            ismonster = "monster"
            if isinstance(lines[currentline], list):
                tempchecks = []
                for line in lines[currentline]:
                    if line[0] == "-":
                        templine = line[1:]
                        toxt = pygame.font.SysFont("Arial", 30).render(templine, True, (255,255,255))
                        tempchecks.append(toxt)
                    else:
                        toxt = pygame.font.SysFont("Arial", 30).render(line, True, (255,255,255))
                        tempchecks.append(toxt)
                if lines[currentline][0][0] == "-":
                    ismonster = "player"
                return (tempchecks, currentline, ismonster, toxt.get_rect())
            
            elif lines[currentline][0] == "-":
                templine = lines[currentline][1:]
                toxt = pygame.font.SysFont("Arial", 30).render(templine, True, (255,255,255))
                return (toxt, currentline, "player", toxt.get_rect())
            else:
                toxt = pygame.font.SysFont("Arial", 30).render(lines[currentline], True, (255,255,255))
                return (toxt, currentline, "monster", toxt.get_rect())
        except IndexError:
            currentline = 0

running = True
clock = pygame.time.Clock()

player = Player()
golem = Golem()

newdialogueline = 0
golemdialogueline = 0
plantdialogueline = 0
wizdialogueline = 0

last = pygame.time.get_ticks()
now = pygame.time.get_ticks()

class ebutton:
    def __init__(self):
        self.image = pygame.image.load('e_button.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.isshowinggolemdialogue = False
        self.isshowingbirddialogue = False
        self.isshowingplantdialogue = False
        self.isshowingshop = False
        self.isshowingwizdialogue = False
        self.rect = self.image.get_rect()

e_button = ebutton()

golem.rect.y = 400

gamestate = "main"

class PIPE:
    def __init__(self):
        self.image = pygame.image.load('pipe.png')
        self.image = pygame.transform.scale(self.image, (40, random.randint(20,250)))
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT/2-150+300
    def move(self, vel):
        self.rect.x += vel
class UPSIDEDOWNPIPE:
    def __init__(self):
        self.image = pygame.image.load('pipe.png')
        self.image = pygame.transform.scale(self.image, (40,random.randint(20,250)))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.top = SCREEN_HEIGHT/2-150
    def move(self, vel):
        self.rect.x += vel
class PIPE3:
    def __init__(self):
        self.image = pygame.image.load('pipe.png')
        self.image = pygame.transform.scale(self.image, (40, random.randint(20,250)))
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT/2-150+300
    def move(self, vel):
        self.rect.x -= vel
leftmostbox = SCREEN_WIDTH/2-150
rightmostbox = SCREEN_WIDTH/2+150

mypipe = PIPE()
mypipe.rect.left = leftmostbox-200

myupsidedownpipe = UPSIDEDOWNPIPE()
myupsidedownpipe.rect.left = leftmostbox-200

my3rdleg = PIPE3()
my3rdleg.rect.right = rightmostbox+200

class BIGBUTTTON:
    def __init__(self,image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (373.8, 133))
        self.rect = self.image.get_rect()


fightbutton = BIGBUTTTON('FIGHTBUTTON.png')

itembutton = BIGBUTTTON('TRUE.jpg')

mercbutton = BIGBUTTTON('MERCBEAST.jpg')

returnbutton = BIGBUTTTON('returnbeast.png')
returnbutton.image = pygame.transform.scale(returnbutton.image, (89, 26))
returnbutton.rect = returnbutton.image.get_rect()

rollx = SCREEN_WIDTH/2-275
my_y = SCREEN_HEIGHT/2-50
tempx = SCREEN_WIDTH/2-275
linegoinleft = False
linestopped = False

hb1 = hitbutton("red", rollx, my_y, 150, 100)
hb2 = hitbutton("yellow", rollx+150, my_y, 100, 100)
hb3 = hitbutton("green", rollx+250, my_y, 50, 100)
hb4 = hitbutton("yellow", rollx+300, my_y, 100, 100)
hb5 = hitbutton("red", rollx+400, my_y, 150, 100)

hbrects = [hb1, hb2, hb3, hb4, hb5]

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Undertale.png')
        self.image = pygame.transform.scale(self.image, (25,25))
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN_WIDTH/2,SCREEN_HEIGHT/2]
    def checks(self, now, newnewlast):
        if gamestats["currentmonster"] != thiswiz:
            if self.rect.left <= SCREEN_WIDTH/2-150:
                self.rect.left = SCREEN_WIDTH/2-150
            if self.rect.right >= SCREEN_WIDTH/2+150:
                self.rect.right = SCREEN_WIDTH/2+150
            if self.rect.top <= SCREEN_HEIGHT/2-150:
                self.rect.top = SCREEN_HEIGHT/2-150
            if self.rect.bottom >= SCREEN_HEIGHT/2+150:
                self.rect.bottom = SCREEN_HEIGHT/2+150
        else:
            if self.rect.left <= gamerect2.left:
                self.rect.left = gamerect2.left
                if now - newnewlast >= 200:
                    player.health -= 1
                    newnewlast = pygame.time.get_ticks()
            if self.rect.right >= gamerect2.right:
                self.rect.right = gamerect2.right
                if now - newnewlast >= 200:
                    player.health -= 1
                    newnewlast = pygame.time.get_ticks()
            if self.rect.top <= gamerect2.top:
                self.rect.top = gamerect2.top
                if now - newnewlast >= 200:
                    player.health -= 1
                    newnewlast = pygame.time.get_ticks()
            if self.rect.bottom >= gamerect2.bottom:
                self.rect.bottom = gamerect2.bottom
                if now - newnewlast >= 200:
                    player.health -= 1
                    newnewlast = pygame.time.get_ticks()
            return newnewlast

leftmostbox = SCREEN_WIDTH/2-150
rightmostbox = SCREEN_WIDTH/2+150
upmostbox = SCREEN_HEIGHT/2-150
downmostbox = SCREEN_HEIGHT/2+150

ischange = False

class Weapon:
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (85,37.5))
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))
    def move(self,vel):
        self.rect.x += vel

class VertWeapon:
    def __init__(self,image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (85,37.5))
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
    def move(self, vel):
        self.rect.y += vel
utheart = Heart()

golclub = Weapon('golemweapon.png')
golclub.rect.left = leftmostbox-200
golclub2 = Weapon('golemweapon.png')
golclub2.image = pygame.transform.rotate(golclub2.image, 180)
golclub2.rect.right = rightmostbox+200
golclub3 = VertWeapon('golemweapon.png')
golclub3.rect.top = upmostbox-200
golclub4 = VertWeapon('golemweapon.png')
golclub4.image = pygame.transform.rotate(golclub4.image, 180)
golclub4.rect.bottom = downmostbox+200

round = 0

class HealthBar:
    def __init__(self):
        self.currenthealth = player.health
    def drawit(self):
        pygame.draw.rect(screen, "red", (0,0,300,75))
        pygame.draw.rect(screen, "green", (0,0,15*self.currenthealth,75))
    def upd(self):
        self.currenthealth = player.health

class MonsterHB:
    def __init__(self, monster):
        self.monster = monster
        self.currenthealth = self.monster.health
    def drawit(self):
        pygame.draw.rect(screen, "red", (SCREEN_WIDTH-300,0,300,75))
        pygame.draw.rect(screen, "green", (SCREEN_WIDTH-300,0,(300/15)*self.currenthealth,75))
    def upd(self):
        self.currenthealth = self.monster.health

tshb = HealthBar()
monstahb = MonsterHB(golem)
birbhb = MonsterHB(birb)
planthb = MonsterHB(planto)
wizhb = MonsterHB(thiswiz)

gamestats = {"currentmonster":golem, "route":"pacifist", "money":0}

playerinv = {}


gamerect1 = pygame.Rect(SCREEN_WIDTH/2-160,SCREEN_HEIGHT/2-160,320,320) #pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-160,SCREEN_HEIGHT/2-160,320,320))
gr1isposx = True
gr1isposy = True
gr2col = "black"

gamerect2 = pygame.Rect(SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2-150,300,300)


shoota = pygame.image.load('peashooter.png')
shoota = pygame.transform.scale(shoota, (442/10, 446/10))
shootarect = shoota.get_rect()


skibidutton = sanbutton()

birb.rect.y = 700

viswidth = 0
camera_group = CameraGroup(tmx_data)

# Add the player to the camera group
player = Player()
camera_group.add(player)
camera_group.add(golem)
camera_group.add(birb)
camera_group.add(skibidutton)
camera_group.add(planto)
camera_group.add(thiswiz)
minime = load_image('Wraith_01_Idle_000.png', (50.25, 72.25))
minigol = load_image('Golem_01_Idle Blinking_000.png', (50.25, 72.25))
sansbutt = load_image("SANS.png", (225, 300))
truesans = load_image("skibidi.png", (1024 // 5, 1346 // 5))
minibird = load_image('birdie000.png', (50.25, 72.25))
miniplant = load_image('plant000.png', (50.25, 72.25))
miniwiz = load_image('wiz000.png', (50.25,72.25))

#75x100
srect = sansbutt.get_rect()
srect.x = SCREEN_WIDTH-srect.w-10
srect.y = SCREEN_HEIGHT/2-srect.h/2
#1024x1346
trrect = truesans.get_rect()
trrect.x = SCREEN_WIDTH/2-trrect.w/2
trrect.y = SCREEN_HEIGHT/2-trrect.h/2
# Load NPC images
sansbutt_image = load_image("SANS.png", (225, 300))
truesans_image = load_image("skibidi.png", (1024 // 5, 1346 // 5))

class Pea:
    def __init__(self):
        self.image = pygame.image.load('pea.png')
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH/2-shootarect.w/2
        self.rect.y = SCREEN_HEIGHT/2+150-shootarect.h
        self.movex = True
        self.movey = True
    def move(self):
        self.rect.x += self.movex
        self.rect.y -= self.movey
    def reset(self):
        self.rect.x = SCREEN_WIDTH/2-shootarect.w/2
        self.rect.y = SCREEN_HEIGHT/2+150-shootarect.h
        self.movex = True
        self.movey = True
    def checks(self):
        if self.rect.right >= SCREEN_WIDTH/2+150:
            self.reset()
        if self.rect.x <= SCREEN_WIDTH/2-150:
            self.reset()
        if self.rect.y <= SCREEN_HEIGHT/2-150:
            self.reset()
        if isinstance(self.movex, bool) and isinstance(self.movey, bool):
            distance = (utheart.rect.centerx-self.rect.centerx, abs(utheart.rect.centery-self.rect.centery))#pygame.Vector2(utheart.rect.center).distance_to(pygame.Vector2(self.rect.center))
            #print(distance)
            self.movey = distance[1]/30
            self.movex = distance[0]/30


testp = Pea()
testp2 = Pea()
testp3 = Pea()
testp4 = Pea()
testp5 = Pea()

incval = 3

peaobjs = [testp, testp2, testp3, testp4, testp5]

# Create NPCs
#sansbutt = NPC(sansbutt_image, SCREEN_WIDTH - 235, SCREEN_HEIGHT // 2 - 150)
#truesans = NPC(truesans_image, SCREEN_WIDTH // 2 - 1024 // 10, SCREEN_HEIGHT // 2 - 1346 // 10)

# Add NPCs to the list
npc_list = [golem, birb]
pygame.mixer.Sound.play(pygame.mixer.Sound("Balatro - Complete Original Soundtrack (Official).mp3"))

mypeeps = [golem, birb, planto, skibidutton, thiswiz]

while running:
    """if player.rect.x > SCREEN_WIDTH /4 *3:
        cameraX -= 5
    elif player.rect.x < SCREEN_WIDTH / 6:
        cameraX += 5"""
    if gamestate == "main":
        
        if current_music != "main":
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_files["main"])
            pygame.mixer.music.play(-1)  # Loop the music
        current_music = "main"
        camera_offset_x = player.rect.centerx - SCREEN_WIDTH // 2
        camera_offset_y = player.rect.centery - SCREEN_HEIGHT // 2
        screen.fill((0, 0, 0))
        # Define camera thresholds
        CAMERA_THRESHOLD_X = SCREEN_WIDTH // 4
        CAMERA_THRESHOLD_Y = SCREEN_HEIGHT // 4

        #print(camera_group.sprites())

        # Calculate camera offset
        if player.rect.centerx > SCREEN_WIDTH - CAMERA_THRESHOLD_X:
            camera_offset_x += player.rect.centerx - (SCREEN_WIDTH - CAMERA_THRESHOLD_X)
        elif player.rect.centerx < CAMERA_THRESHOLD_X:
            camera_offset_x += player.rect.centerx - CAMERA_THRESHOLD_X

        if player.rect.centery > SCREEN_HEIGHT - CAMERA_THRESHOLD_Y:
            camera_offset_y += player.rect.centery - (SCREEN_HEIGHT - CAMERA_THRESHOLD_Y)
        elif player.rect.centery < CAMERA_THRESHOLD_Y:
            camera_offset_y += player.rect.centery - CAMERA_THRESHOLD_Y
        # Camera.box_target_camera(Player.rect, SCREEN_WIDTH, SCREEN_HEIGHT)
        sprite_group.draw(screen)
        camera_group.custom_draw(player, mypeeps, e_button)
       # screen.blit(player.image, (player.rect.x, player.rect.y))

        #print(player.rect.y)

        thisfont = pygame.font.SysFont("Arial", 30)
        thistxt = "Coins: " + str(gamestats["money"])
        mytxt = thisfont.render(thistxt, True, "white")
        screen.blit(mytxt, (10,10))
        
        #pygame.draw.rect(screen, "red", (player.rect.x, player.rect.y, player.rect.w, player.rect.h)
        

        #pygame.draw.rect(screen, (255,255,255), (player.rect.x, player.rect.y, player.rect.w, player.rect.h))

        # screen.blit(player.image, (player.rect.x, player.rect.y))

        """if player.rect.right >= SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
        if player.rect.x <= 0:
            player.rect.x = 0
        if player.rect.y <= 0:
            player.rect.y = 0
        if player.rect.bottom >= SCREEN_HEIGHT:
            player.rect.bottom = SCREEN_HEIGHT"""
        
        #screen.blit(sansbutt, (srect.x, srect.y))

        expansion = player.rect.inflate(50,50)

        if expansion.colliderect(skibidutton.rect):
            erect = e_button.image.get_rect()
            screen.blit(e_button.image, (-10000,-100000))
            e_button.isshowingshop=True
        else:
            e_button.isshowingshop = False

        #if player.rect.colliderect(skibidutton.rect):
            #docollisions(skibidutton.rect)

        #if not(player.isplantdefeated):
            #y = golemdialogue()

        if not(player.isplantdefeated) and not(planto.isdefeated):
            y = golemdialogue(plantdialogueline, "planty.npc")

            plantdialogueline = y[1]

            planttxtrct = y[3]

            planto.idleanimation()
            if expansion.colliderect(planto.rect):
                #screen.blit(e_button.image, (planto.rect.x+50,planto.rect.y))
                if y[2] == "monster":
                    pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-300,SCREEN_HEIGHT-250,600,200))
                    tsrect = pygame.draw.rect(screen, "black", (SCREEN_WIDTH/2-290,SCREEN_HEIGHT-240,580,180))
                    screen.blit(miniplant, (SCREEN_WIDTH/2-280,tsrect.centery-36.125))
                    if isinstance(y[0], list):
                        screen.blit(y[0][0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                        screen.blit(y[0][1], (SCREEN_WIDTH/2-280+50.25+25,SCREEN_HEIGHT-200))
                    else:
                        screen.blit(y[0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                elif y[2] == "player":
                    pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-300,SCREEN_HEIGHT-250,600,200))
                    pygame.draw.rect(screen, "black", (SCREEN_WIDTH/2-290,SCREEN_HEIGHT-240,580,180))
                    screen.blit(minime, (SCREEN_WIDTH/2-280,tsrect.centery-36.125))
                    if isinstance(y[0], list):
                        screen.blit(y[0][0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                        screen.blit(y[0][1], (SCREEN_WIDTH/2-280+50.25+25,SCREEN_HEIGHT-200))
                    else:
                        screen.blit(y[0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                e_button.isshowingplantdialogue = True
            else:
                e_button.isshowingplantdialogue = False
                plantdialogueline = 0
            #if player.rect.colliderect(planto.rect):
                #docollisions(planto.rect)

        if not(player.iswizdefeated) and not(thiswiz.isdefeated):
            w = golemdialogue(wizdialogueline, "planty.npc")

            wizdialogueline = w[1]

            wiztxtrct = w[3]

            thiswiz.idleanimation()
            if expansion.colliderect(thiswiz.rect):
                #screen.blit(e_button.image, (planto.rect.x+50,planto.rect.y))
                if w[2] == "monster":
                    pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-300,SCREEN_HEIGHT-250,600,200))
                    tsrect = pygame.draw.rect(screen, "black", (SCREEN_WIDTH/2-290,SCREEN_HEIGHT-240,580,180))
                    screen.blit(miniwiz, (SCREEN_WIDTH/2-280,tsrect.centery-36.125))
                    if isinstance(w[0], list):
                        screen.blit(w[0][0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                        screen.blit(w[0][1], (SCREEN_WIDTH/2-280+50.25+25,SCREEN_HEIGHT-200))
                    else:
                        screen.blit(w[0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                elif w[2] == "player":
                    pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-300,SCREEN_HEIGHT-250,600,200))
                    pygame.draw.rect(screen, "black", (SCREEN_WIDTH/2-290,SCREEN_HEIGHT-240,580,180))
                    screen.blit(minime, (SCREEN_WIDTH/2-280,tsrect.centery-36.125))
                    if isinstance(w[0], list):
                        screen.blit(w[0][0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                        screen.blit(w[0][1], (SCREEN_WIDTH/2-280+50.25+25,SCREEN_HEIGHT-200))
                    else:
                        screen.blit(w[0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                e_button.isshowingwizdialogue = True
            else:
                e_button.isshowingwizdialogue = False
                wizdialogueline = 0
            #if player.rect.colliderect(planto.rect):
                #docollisions(planto.rect)

        if not(player.isbirddefeated) and not(birb.isdefeated):

            z = golemdialogue(newdialogueline, "birddialogue.npc")

            newdialogueline = z[1]

            newtxtrct = z[3]

            

            #screen.blit(birb.image, (birb.rect.x,birb.rect.y))
            #camera_group.custom_draw(birb)
            birb.idleanimation()
            if expansion.colliderect(birb.rect):
                #screen.blit(e_button.image, (birb.rect.x+50,birb.rect.y))
                if z[2] == "monster":
                    pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-300,SCREEN_HEIGHT-250,600,200))
                    tsrect = pygame.draw.rect(screen, "black", (SCREEN_WIDTH/2-290,SCREEN_HEIGHT-240,580,180))
                    screen.blit(minibird, (SCREEN_WIDTH/2-280,tsrect.centery-36.125))
                    if isinstance(z[0], list):
                        screen.blit(z[0][0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                        screen.blit(z[0][1], (SCREEN_WIDTH/2-280+50.25+25,SCREEN_HEIGHT-200))
                    else:
                        screen.blit(z[0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                elif z[2] == "player":
                    pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-300,SCREEN_HEIGHT-250,600,200))
                    pygame.draw.rect(screen, "black", (SCREEN_WIDTH/2-290,SCREEN_HEIGHT-240,580,180))
                    screen.blit(minime, (SCREEN_WIDTH/2-280,tsrect.centery-36.125))
                    if isinstance(z[0], list):
                        screen.blit(z[0][0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                        screen.blit(z[0][1], (SCREEN_WIDTH/2-280+50.25+25,SCREEN_HEIGHT-200))
                    else:
                        screen.blit(z[0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                e_button.isshowingbirddialogue = True
            else:
                e_button.isshowingbirddialogue = False
                newdialogueline = 0
            #if player.rect.colliderect(birb.rect):
                #docollisions(birb.rect)

        if not(player.isgolemdefeated) and not(golem.isdefeated):

            x = golemdialogue(golemdialogueline, "golemtext.npc")

            golemdialogueline = x[1]

            txtrct = x[3]

            golem.idleanimation()

            #screen.blit(golem.image, (golem.rect.x, golem.rect.y))

            if expansion.colliderect(golem.rect):
                #screen.blit(e_button.image, (golem.rect.x+50,golem.rect.y-60))
                if x[2] == "monster":
                    pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-300,SCREEN_HEIGHT-250,600,200))
                    tsrect = pygame.draw.rect(screen, "black", (SCREEN_WIDTH/2-290,SCREEN_HEIGHT-240,580,180))
                    screen.blit(minigol, (SCREEN_WIDTH/2-280,tsrect.centery-36.125))
                    if isinstance(x[0], list):
                        screen.blit(x[0][0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                        screen.blit(x[0][1], (SCREEN_WIDTH/2-280+50.25+25,SCREEN_HEIGHT-200))
                    else:
                        screen.blit(x[0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                elif x[2] == "player":
                    pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-300,SCREEN_HEIGHT-250,600,200))
                    pygame.draw.rect(screen, "black", (SCREEN_WIDTH/2-290,SCREEN_HEIGHT-240,580,180))
                    screen.blit(minime, (SCREEN_WIDTH/2-280,tsrect.centery-36.125))
                    if isinstance(x[0], list):
                        screen.blit(x[0][0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                        screen.blit(x[0][1], (SCREEN_WIDTH/2-280+50.25+25,SCREEN_HEIGHT-200))
                    else:
                        screen.blit(x[0], (SCREEN_WIDTH/2-280+50.25,SCREEN_HEIGHT-230))
                e_button.isshowinggolemdialogue = True
            else:
                e_button.isshowinggolemdialogue = False
                golemdialogueline = 0

            #if player.rect.colliderect(golem.rect):
                #docollisions(golem.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYUP:
                player.ismoving = False
                player.goingup = False
                player.goingdown = False
                player.goingleft = False
                player.goingright = False

        key = pygame.key.get_pressed()
        
        if key[pygame.K_UP]:
            player.goingup = True
            player.rect.y -= 7
            player.movement()
        elif key[pygame.K_DOWN]:
            player.goingdown = True
            player.rect.y += 7
            player.movement()
        elif key[pygame.K_LEFT]:
            player.goingleft = True
            player.rect.x -= 7
            player.isleft = True
            player.movement()
        elif key[pygame.K_RIGHT]:
            player.goingright = True
            player.rect.x += 7
            player.isleft = False
            player.movement()
        if not(player.ismoving):
            player.idleanimation()
        if key[pygame.K_e] and e_button.isshowinggolemdialogue:
            if now - last >= 700:
                last = pygame.time.get_ticks()
                if golemdialogueline == 5:
                    golemdialogueline = 0
                    gamestate = "fight"
                    gamestats["currentmonster"] = golem
                    e_button.isshowinggolemdialogue = False
                    continue
                golemdialogueline += 1
        if key[pygame.K_e] and e_button.isshowingbirddialogue:
            if now - last >= 700:
                last = pygame.time.get_ticks()
                if newdialogueline == 5:
                    newdialogueline = 0
                    gamestate="fight"
                    gamestats["currentmonster"] = birb
                    e_button.isshowingbirddialogue = False
                    continue
                newdialogueline += 1
        if key[pygame.K_e] and e_button.isshowingplantdialogue:
            if now - last >= 700:
                last = pygame.time.get_ticks()
                if plantdialogueline == 5:
                    plantdialogueline = 0
                    gamestate="fight"
                    gamestats["currentmonster"] = planto
                    e_button.isshowingplantdialogue = False
                    continue
                plantdialogueline += 1
        if key[pygame.K_e] and e_button.isshowingwizdialogue:
            if now - last >= 700:
                last = pygame.time.get_ticks()
                if wizdialogueline == 5:
                    wizdialogueline = 0
                    gamestate="fight"
                    gamestats["currentmonster"] = thiswiz
                    e_button.isshowingwizdialogue = False
                    continue
                wizdialogueline += 1
        if key[pygame.K_e] and e_button.isshowingshop:
            gamestate = "shop"
            continue

        pygame.display.flip()

        clock.tick(60)

        now = pygame.time.get_ticks()

    elif gamestate == "fight":
        if current_music != "fight":
            if pygame.mixer.music.get_busy():  # Check if music is currently playing
                pygame.mixer.music.fadeout(500)  # Fade out the current music over 500ms
            pygame.mixer.music.load(music_files["fight"])  # Load the fight music
            pygame.mixer.music.play(-1)  # Play the fight music in a loop
            current_music = "fight"
        screen.fill("black")

        tshb.upd()
        tshb.drawit()
        
        if gamestats["currentmonster"] == golem:
            monstahb.upd()
            monstahb.drawit()
        elif gamestats["currentmonster"] == birb:
            birbhb.upd()
            birbhb.drawit()
        elif gamestats["currentmonster"] == planto:
            planthb.upd()
            planthb.drawit()
        elif gamestats["currentmonster"] == thiswiz:
            wizhb.upd()
            wizhb.drawit()

        gamestats["currentmonster"].idleanimation()

        gamestats["currentmonster"].fakex = SCREEN_WIDTH/2-100
        gamestats["currentmonster"].fakey = 200

        screen.blit(fightbutton.image, (fightbutton.rect.x,fightbutton.rect.y))
        screen.blit(itembutton.image, (itembutton.rect.x, itembutton.rect.y))
        screen.blit(mercbutton.image, (mercbutton.rect.x, mercbutton.rect.y))

        screen.blit(gamestats["currentmonster"].image, (gamestats['currentmonster'].fakex, gamestats["currentmonster"].fakey))

        fightbutton.rect.x = SCREEN_WIDTH/2-635.7
        fightbutton.rect.y = 500

        itembutton.rect.x = SCREEN_WIDTH/2-635.7+fightbutton.rect.w+50
        itembutton.rect.y = 500

        mercbutton.rect.x = SCREEN_WIDTH/2-635.7+fightbutton.rect.w+50+itembutton.rect.w+50
        mercbutton.rect.y = 500

        #25INCHMARGINS
        
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fightbutton.rect.collidepoint(mouse):
                    gamestate = "attack"
                    continue
                elif itembutton.rect.collidepoint(mouse):
                    gamestate = "item"
                    continue
                elif mercbutton.rect.collidepoint(mouse):
                    gamestate = "mercy"
                    continue
        
        pygame.display.flip()

        clock.tick(60)

        now = pygame.time.get_ticks()

    elif gamestate == "attack":
        screen.fill((0,0,0))

        gamestats["currentmonster"].idleanimation()

        screen.blit(gamestats["currentmonster"].image, (gamestats["currentmonster"].fakex, gamestats["currentmonster"].fakey))

        tshb.upd()
        tshb.drawit()

        if gamestats["currentmonster"] == golem:
            monstahb.upd()
            monstahb.drawit()
        elif gamestats["currentmonster"] == birb:
            birbhb.upd()
            birbhb.drawit()
        elif gamestats["currentmonster"] == planto:
            planthb.upd()
            planthb.drawit()
        elif gamestats["currentmonster"] == thiswiz:
            wizhb.upd()
            wizhb.drawit()

        #print(gamestate)

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE] or key[pygame.K_e]:
            linestopped = True
            for i in hbrects:
                if tempx >= i.x and tempx <= (i.x + i.width):
                    thiscolor = i.color
            if thiscolor == "red":
                gamestats["currentmonster"].health -= 1
            elif thiscolor == "yellow":
                gamestats["currentmonster"].health -= 2
            elif thiscolor == "green":
                gamestats["currentmonster"].health -= 3
            if gamestats["currentmonster"].health <= 0:
                gamestate = "main"
                if gamestats["currentmonster"] == golem:
                    player.isgolemdefeated = True
                    golem.isdefeated = True
                elif gamestats["currentmonster"] == birb:
                    player.isbirddefeated = True
                    birb.isdefeated = True
                elif gamestats["currentmonster"] == planto:
                    player.isplantdefeated = True
                    planto.isdefeated = True
                elif gamestats["currentmonster"] == thiswiz:
                    player.iswizdefeated = True
                    thiswiz.isdefeated = True
                tempx = SCREEN_WIDTH/2-275
                linegoinleft = False
                linestopped = False
                gamestats["currentmonster"].health = 15
                gamestats["money"] += 5
                round = 0
                last = pygame.time.get_ticks()
                continue
            #print("ok")
            tempx = SCREEN_WIDTH/2-275
            linegoinleft = False
            last = pygame.time.get_ticks()
            gamestate = "defend"
            #if gamestats["currentmonster"] == planto:
                #planto.movey = randint(2+round,round*2+4)
            newlast = pygame.time.get_ticks()
            newnewlast = pygame.time.get_ticks()
            round += 1
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                linestopped = True
                for i in hbrects:
                    if tempx >= i.x and tempx <= (i.x + i.width):
                        thiscolor = i.color
                if thiscolor == "red":
                    gamestats["currentmonster"].health -= 1
                elif thiscolor == "yellow":
                    gamestats["currentmonster"].health -= 2
                elif thiscolor == "green":
                    gamestats["currentmonster"].health -= 3
                if gamestats["currentmonster"].health <= 0:
                    gamestate = "main"
                    if gamestats["currentmonster"] == golem:
                        player.isgolemdefeated = True
                        golem.isdefeated = True
                    elif gamestats["currentmonster"] == birb:
                        player.isbirddefeated = True
                        birb.isdefeated = True
                    elif gamestats["currentmonster"] == planto:
                        player.isplantdefeated = True
                        planto.isdefeated = True
                    elif gamestats["currentmonster"] == thiswiz:
                        player.iswizdefeated = True
                        thiswiz.isdefeated = True
                    tempx = SCREEN_WIDTH/2-275
                    linegoinleft = False
                    linestopped = False
                    gamestats["currentmonster"].health = 15
                    gamestats["money"] += 5
                    round = 0
                    last = pygame.time.get_ticks()
                    continue
                #print("ok")
                tempx = SCREEN_WIDTH/2-275
                linegoinleft = False
                last = pygame.time.get_ticks()
                gamestate = "defend"
                #if gamestats["currentmonster"] == planto:
                #    planto.movey = randint(2+round,round*2+4)
                newlast = pygame.time.get_ticks()
                newnewlast = pygame.time.get_ticks()
                round += 1
                continue
                
        pygame.draw.rect(screen, hb1.color, (hb1.x, hb1.y, hb1.width, hb1.height))
        pygame.draw.rect(screen, hb2.color, (hb2.x, hb2.y, hb2.width, hb2.height))
        pygame.draw.rect(screen, hb3.color, (hb3.x, hb3.y, hb3.width, hb3.height))
        pygame.draw.rect(screen, hb4.color, (hb4.x, hb4.y, hb4.width, hb4.height))
        pygame.draw.rect(screen, hb5.color, (hb5.x, hb5.y, hb5.width, hb5.height))
        pygame.draw.line(screen, "white", (tempx,SCREEN_HEIGHT/2-75), (tempx,SCREEN_HEIGHT/2+75), 3)
        if tempx == SCREEN_WIDTH/2+275 and not(linestopped):
            linegoinleft = True
        if tempx == SCREEN_WIDTH/2-275 and not(linestopped):
            linegoinleft = False
        if linegoinleft and not(linestopped):
            tempx-=5
        elif not(linegoinleft) and not(linestopped):
            tempx+=5

        pygame.display.flip()

        clock.tick(60)

        now = pygame.time.get_ticks()

    elif gamestate == "mercy":

        matchcol = "white"

        if round >= 0:
            matchcol = "yellow"

        myman = 0

        myfont = pygame.font.SysFont("Arial", 30)

        mouse = pygame.mouse.get_pos()

        screen.fill((0,0,0))

        tshb.upd()
        tshb.drawit()

        if gamestats["currentmonster"] == golem:
            monstahb.upd()
            monstahb.drawit()
        elif gamestats["currentmonster"] == birb:
            birbhb.upd()
            birbhb.drawit()
        elif gamestats["currentmonster"] == planto:
            planthb.upd()
            planthb.drawit()
        elif gamestats["currentmonster"] == thiswiz:
            wizhb.upd()
            wizhb.drawit()

        gamestats["currentmonster"].idleanimation()

        screen.blit(gamestats["currentmonster"].image, (gamestats["currentmonster"].fakex, gamestats["currentmonster"].fakey))

        blackx = SCREEN_WIDTH/2-390
        blacky = SCREEN_HEIGHT-640

        returnbutton.rect.x = blackx
        returnbutton.rect.y = blacky+254

        mytxt = pygame.font.SysFont("Arial", 30).render("Spare", True, matchcol)
        myrct = mytxt.get_rect()
        myrct.x = SCREEN_WIDTH/2-myrct.w/2
        myrct.y = SCREEN_HEIGHT-640+140-myrct.h/2

        pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-400,SCREEN_HEIGHT-650,800,300))
        pygame.draw.rect(screen, "black", (blackx,blacky,780,280))
        screen.blit(returnbutton.image, (returnbutton.rect.x,returnbutton.rect.y))
        screen.blit(mytxt, (myrct.x, myrct.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if returnbutton.rect.collidepoint(mouse):
                    gamestate="fight"
                    continue
                if myrct.collidepoint(mouse):
                    if matchcol == "white":
                        last = pygame.time.get_ticks()
                        newlast = pygame.time.get_ticks()
                        newnewlast = pygame.time.get_ticks()
                        gamestate = "defend"
                        #if gamestats["currentmonster"] == planto:
                        #    planto.movey = randint(2+round,round*2+4)
                        round += 1
                        continue
                    elif matchcol == "yellow":
                        gamestate = "main"
                        if gamestats["currentmonster"] == golem:
                            player.isgolemdefeated = True
                            golem.isdefeated = True
                        elif gamestats["currentmonster"] == birb:
                            player.isbirddefeated = True
                            birb.isdefeated = True
                        elif gamestats["currentmonster"] == planto:
                            player.isplantdefeated = True
                            planto.isdefeated = True
                        elif gamestats["currentmonster"] == thiswiz:
                            player.iswizdefeated = True
                            thiswiz.isdefeated = True
                        tempx = SCREEN_WIDTH/2-275
                        linegoinleft = False
                        linestopped = False
                        gamestats["currentmonster"].health = 15
                        gamestats["money"] += 5
                        round = 0
                        last = pygame.time.get_ticks()
                        continue

        pygame.display.flip()

        clock.tick(60)

        now = pygame.time.get_ticks()

    elif gamestate == "item":

        myman = 0

        myfont = pygame.font.SysFont("Arial", 30)

        mouse = pygame.mouse.get_pos()

        screen.fill((0,0,0))

        tshb.upd()
        tshb.drawit()

        if gamestats["currentmonster"] == golem:
            monstahb.upd()
            monstahb.drawit()
        elif gamestats["currentmonster"] == birb:
            birbhb.upd()
            birbhb.drawit()
        elif gamestats["currentmonster"] == planto:
            planthb.upd()
            planthb.drawit()
        elif gamestats["currentmonster"] == thiswiz:
            wizhb.upd()
            wizhb.drawit()

        gamestats["currentmonster"].idleanimation()

        screen.blit(gamestats["currentmonster"].image, (gamestats["currentmonster"].fakex, gamestats["currentmonster"].fakey))

        blackx = SCREEN_WIDTH/2-390
        blacky = SCREEN_HEIGHT-640

        returnbutton.rect.x = blackx
        returnbutton.rect.y = blacky+254

        pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-400,SCREEN_HEIGHT-650,800,300))
        pygame.draw.rect(screen, "black", (blackx,blacky,780,280))
        screen.blit(returnbutton.image, (returnbutton.rect.x,returnbutton.rect.y))

        myrects = []
        mifontes = []

        for item in playerinv:
            thistext = {"text":myfont.render((playerinv.get(item))[0]+" - +" + str((playerinv.get(item))[1]) + " HP", True, (255,255,255)),"rect":0}
            tsrectt = thistext["text"].get_rect()
            tsrectt.x = blackx
            tsrectt.y = blacky+myman
            thistext["rect"] = tsrectt
            myrects.append(tsrectt)
            mifontes.append(thistext)
            screen.blit(thistext["text"], (thistext["rect"].x, thistext["rect"].y))
            myman+=tsrectt.h+10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if returnbutton.rect.collidepoint(mouse):
                    gamestate="fight"
                    continue
                for i in myrects:
                    if i.collidepoint(mouse):
                        for z in mifontes:
                            if z["rect"].x == i.x and z["rect"].y == i.y:
                                thishlth = list(playerinv.values())[mifontes.index(z)][1]
                                playerinv.pop(list(playerinv.keys())[mifontes.index(z)])
                        last = pygame.time.get_ticks()
                        newlast = pygame.time.get_ticks()
                        newnewlast = pygame.time.get_ticks()
                        gamestate = "defend"
                        #if gamestats["currentmonster"] == planto:
                        #    planto.movey = randint(2+round,round*2+4)
                        round += 1
                        player.health += thishlth
                        if player.health > 20:
                            player.health =20
                        continue

        pygame.display.flip()

        clock.tick(60)

        now = pygame.time.get_ticks()

    elif gamestate == "defend":

        if gamestats["currentmonster"] == thiswiz:
            screen.fill("black")

            thiswiz.idleanimation()

            screen.blit(thiswiz.image, (thiswiz.fakex, thiswiz.fakey))

            tshb.upd()
            tshb.drawit()

            if gamestats["currentmonster"] == golem:
                monstahb.upd()
                monstahb.drawit()
            elif gamestats["currentmonster"] == birb:
                birbhb.upd()
                birbhb.drawit()
            elif gamestats["currentmonster"] == planto:
                planthb.upd()
                planthb.drawit()
            elif gamestats["currentmonster"] == thiswiz:
                wizhb.upd()
                wizhb.drawit()

            x=utheart.checks(now, newnewlast)
            newnewlast = x

            if player.health == 0:
                running = False
                break

            pygame.draw.rect(screen, "white", gamerect1)

            pygame.draw.rect(screen, gr2col, gamerect2)

            #screen.blit(shoota, (SCREEN_WIDTH/2-shootarect.w/2,SCREEN_HEIGHT/2+150-shootarect.h))

            if now-newlast >= 11500:
                utheart.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
                gamerect1.x = SCREEN_WIDTH/2-160
                gamerect2.x = SCREEN_WIDTH/2-150
                gamerect1.y = SCREEN_HEIGHT/2-160
                gamerect2.y = SCREEN_HEIGHT/2-150
                gr2col = "black"
                #for testp in peaobjs:
                #    testp.reset()
                """
                golclub2.rect.right = rightmostbox+200
                golclub2.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))
                golclub3.rect.top = upmostbox-200
                golclub3.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                golclub4.rect.bottom = downmostbox+200
                golclub4.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                """
                gamestate = "fight"
                tempx = SCREEN_WIDTH/2-275
                linegoinleft = False
                linestopped = False
                continue

            if now-last >= 1500:
                if round >= 4:
                    incval = 5
                elif round >= 3:
                    incval = 4
                elif round >= 2:
                    incval = 3
                else:
                    incval = 2
                if gr1isposx:
                    gamerect2.x+=incval
                    gamerect1.x+=incval
                else:
                    gamerect2.x-=incval
                    gamerect1.x-=incval
                if gr1isposy:
                    gamerect2.y+=incval
                    gamerect1.y+=incval
                else:
                    gamerect2.y-=incval
                    gamerect1.y-=incval
                if gamerect1.right >= SCREEN_WIDTH:
                    gr1isposx = False
                    gr2col = random.choice(cols)
                if gamerect1.left <= 0:
                    gr1isposx = True
                    gr2col = random.choice(cols)
                if gamerect1.top <= 0:
                    gr1isposy = True
                    gr2col = random.choice(cols)
                if gamerect1.bottom >= SCREEN_HEIGHT:
                    gr1isposy = False
                    gr2col = random.choice(cols)

            screen.blit(utheart.image, (utheart.rect.x, utheart.rect.y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            key = pygame.key.get_pressed()
            
            if key[pygame.K_UP]:
                utheart.rect.y -= 9
            if key[pygame.K_DOWN]:
                utheart.rect.y += 9
            if key[pygame.K_LEFT]:
                utheart.rect.x -= 9
            if key[pygame.K_RIGHT]:
                utheart.rect.x += 9
            
            pygame.display.flip()

            clock.tick(60)

            now = pygame.time.get_ticks()

        elif gamestats["currentmonster"] == planto:
            screen.fill("black")

            planto.idleanimation()

            screen.blit(planto.image, (planto.fakex, planto.fakey))

            tshb.upd()
            tshb.drawit()

            if gamestats["currentmonster"] == golem:
                monstahb.upd()
                monstahb.drawit()
            elif gamestats["currentmonster"] == birb:
                birbhb.upd()
                birbhb.drawit()
            elif gamestats["currentmonster"] == planto:
                planthb.upd()
                planthb.drawit()

            utheart.checks(now,newlast)

            pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-160,SCREEN_HEIGHT/2-160,320,320))

            pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2-150,300,300))

            screen.blit(shoota, (SCREEN_WIDTH/2-shootarect.w/2,SCREEN_HEIGHT/2+150-shootarect.h))

            if now-newlast >= 11500:
                utheart.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
                for testp in peaobjs:
                    testp.reset()
                """
                golclub2.rect.right = rightmostbox+200
                golclub2.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))
                golclub3.rect.top = upmostbox-200
                golclub3.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                golclub4.rect.bottom = downmostbox+200
                golclub4.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                """
                gamestate = "fight"
                tempx = SCREEN_WIDTH/2-275
                linegoinleft = False
                linestopped = False
                continue

            if now-last >= 1500:
                for testp in peaobjs:

                    screen.blit(testp.image, (testp.rect.x,testp.rect.y))

                    testp.move()
                    testp.checks()
                    if utheart.rect.colliderect(testp.rect):
                        sound_effects_channel.play(metal_pipe_sound)
                        player.health -= 2
                        if player.health == 0:
                            gamestate = "gameover"
                            last = pygame.time.get_ticks()
                            continue
                        for testp in peaobjs:
                            testp.reset()
                        """
                        golclub2.rect.right = rightmostbox+200
                        golclub2.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))
                        golclub3.rect.top = upmostbox-200
                        golclub3.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                        golclub4.rect.bottom = downmostbox+200
                        golclub4.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                        """

            """

            if golclub3.rect.bottom >= downmostbox+200:
                golclub3.rect.top = upmostbox-200
                golclub3.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))

            if golclub4.rect.top <= upmostbox-200:
                golclub4.rect.bottom = downmostbox+200
                golclub4.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))

            """

            screen.blit(utheart.image, (utheart.rect.x, utheart.rect.y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            key = pygame.key.get_pressed()
            
            if key[pygame.K_UP]:
                utheart.rect.y -= 6
            if key[pygame.K_DOWN]:
                utheart.rect.y += 6
            if key[pygame.K_LEFT]:
                utheart.rect.x -= 6
            if key[pygame.K_RIGHT]:
                utheart.rect.x += 6
            
            pygame.display.flip()

            clock.tick(60)

            now = pygame.time.get_ticks()

        elif gamestats["currentmonster"] == birb:
            screen.fill("black")

            while mypipe.rect.h + myupsidedownpipe.rect.h > 250 or mypipe.rect.h + myupsidedownpipe.rect.h < 225:
                myupsidedownpipe.image = pygame.image.load('pipe.png')
                myupsidedownpipe.image = pygame.transform.rotate(myupsidedownpipe.image, 180)
                myupsidedownpipe.image = pygame.transform.scale(myupsidedownpipe.image, (40,random.randint(1,250)))
                myupsidedownpipe.rect = myupsidedownpipe.image.get_rect()
                myupsidedownpipe.rect.top = SCREEN_HEIGHT/2-150
                myupsidedownpipe.rect.left = leftmostbox-200

            birb.idleanimation()

            screen.blit(birb.image, (birb.fakex, birb.fakey))

            tshb.upd()
            tshb.drawit()

            if gamestats["currentmonster"] == golem:
                monstahb.upd()
                monstahb.drawit()
            elif gamestats["currentmonster"] == birb:
                birbhb.upd()
                birbhb.drawit()
            elif gamestats["currentmonster"] == planto:
                planthb.upd()
                planthb.drawit()

            utheart.checks(now,newlast)

            pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-160,SCREEN_HEIGHT/2-160,320,320))

            pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2-150,300,300))

            if now-newlast >= 11500:
                utheart.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
                mypipe.image = pygame.transform.scale(mypipe.image, (40, random.randint(20,250)))
                mypipe.rect = mypipe.image.get_rect()
                mypipe.rect.bottom = SCREEN_HEIGHT/2-150+300
                mypipe.rect.left = leftmostbox-200
                myupsidedownpipe.image = pygame.transform.scale(myupsidedownpipe.image, (40,random.randint(1,250)))
                myupsidedownpipe.rect = myupsidedownpipe.image.get_rect()
                myupsidedownpipe.rect.top = SCREEN_HEIGHT/2-150
                myupsidedownpipe.rect.left = leftmostbox-200
                """
                golclub2.rect.right = rightmostbox+200
                golclub2.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))
                golclub3.rect.top = upmostbox-200
                golclub3.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                golclub4.rect.bottom = downmostbox+200
                golclub4.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                """
                gamestate = "fight"
                tempx = SCREEN_WIDTH/2-275
                linegoinleft = False
                linestopped = False
                continue

            if now-last >= 1500:
                if mypipe.rect.x >= SCREEN_WIDTH/2-150 and mypipe.rect.right <= SCREEN_WIDTH/2+150:
                    screen.blit(mypipe.image, (mypipe.rect.x,mypipe.rect.y))
                mypipe.move((round+1)*1.5)
                if myupsidedownpipe.rect.x >= SCREEN_WIDTH/2-150 and myupsidedownpipe.rect.right <= SCREEN_WIDTH/2+150:
                    screen.blit(myupsidedownpipe.image, (myupsidedownpipe.rect.x, myupsidedownpipe.rect.y))
                myupsidedownpipe.move((round+1)*1.5)
                """
                if round >= 2:
                    screen.blit(golclub2.image, (golclub2.rect.x,golclub2.rect.y))
                    golclub2.move(-5)
                if round >= 3:
                    screen.blit(golclub3.image, (golclub3.rect.x,golclub3.rect.y))
                    golclub3.move(5)
                if round >= 4:
                    screen.blit(golclub4.image, (golclub4.rect.x,golclub4.rect.y))
                    golclub4.move(-5)
                """
                if utheart.rect.colliderect(mypipe.rect) or utheart.rect.colliderect(myupsidedownpipe.rect):
                    sound_effects_channel.play(metal_pipe_sound)
                    player.health -= 2
                    if player.health == 0:
                        gamestate = "gameover"
                        last = pygame.time.get_ticks()
                        continue
                    mypipe.image = pygame.transform.scale(mypipe.image, (40, random.randint(20,250)))
                    mypipe.rect = mypipe.image.get_rect()
                    mypipe.rect.bottom = SCREEN_HEIGHT/2-150+300
                    mypipe.rect.left = leftmostbox-200
                    myupsidedownpipe.image = pygame.transform.scale(myupsidedownpipe.image, (40,random.randint(20,250)))
                    myupsidedownpipe.rect = myupsidedownpipe.image.get_rect()
                    myupsidedownpipe.rect.top = SCREEN_HEIGHT/2-150
                    myupsidedownpipe.rect.left = leftmostbox-200
                    """
                    golclub2.rect.right = rightmostbox+200
                    golclub2.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))
                    golclub3.rect.top = upmostbox-200
                    golclub3.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                    golclub4.rect.bottom = downmostbox+200
                    golclub4.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                    """

            if mypipe.rect.right >= rightmostbox+200:
                mypipe.image = pygame.transform.scale(mypipe.image, (40, random.randint(20,250)))
                mypipe.rect = mypipe.image.get_rect()
                mypipe.rect.bottom = SCREEN_HEIGHT/2-150+300
                mypipe.rect.left = leftmostbox-200

            if myupsidedownpipe.rect.right >= rightmostbox+200:
                myupsidedownpipe.image = pygame.transform.scale(myupsidedownpipe.image, (40,random.randint(20,250)))
                myupsidedownpipe.rect = myupsidedownpipe.image.get_rect()
                myupsidedownpipe.rect.top = SCREEN_HEIGHT/2-150
                myupsidedownpipe.rect.left = leftmostbox-200

            """

            if golclub3.rect.bottom >= downmostbox+200:
                golclub3.rect.top = upmostbox-200
                golclub3.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))

            if golclub4.rect.top <= upmostbox-200:
                golclub4.rect.bottom = downmostbox+200
                golclub4.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))

            """

            screen.blit(utheart.image, (utheart.rect.x, utheart.rect.y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            key = pygame.key.get_pressed()
            
            if key[pygame.K_UP]:
                utheart.rect.y -= 6
            if key[pygame.K_DOWN]:
                utheart.rect.y += 6
            if key[pygame.K_LEFT]:
                utheart.rect.x -= 6
            if key[pygame.K_RIGHT]:
                utheart.rect.x += 6
            
            pygame.display.flip()

            clock.tick(60)

            now = pygame.time.get_ticks()

        elif gamestats["currentmonster"] == golem:
            screen.fill("black")

            golem.idleanimation()

            screen.blit(golem.image, (golem.fakex, golem.fakey))

            tshb.upd()
            tshb.drawit()

            if gamestats["currentmonster"] == golem:
                monstahb.upd()
                monstahb.drawit()
            elif gamestats["currentmonster"] == birb:
                birbhb.upd()
                birbhb.drawit()
            elif gamestats["currentmonster"] == planto:
                planthb.upd()
                planthb.drawit()

            utheart.checks(now,newlast)

            pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-160,SCREEN_HEIGHT/2-160,320,320))

            pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2-150,300,300))

            if now-newlast >= 11500:
                utheart.rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
                golclub.rect.left = leftmostbox-200
                golclub.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))
                golclub2.rect.right = rightmostbox+200
                golclub2.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))
                golclub3.rect.top = upmostbox-200
                golclub3.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                golclub4.rect.bottom = downmostbox+200
                golclub4.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                gamestate = "fight"
                tempx = SCREEN_WIDTH/2-275
                linegoinleft = False
                linestopped = False
                continue

            if now-last >= 1500:
                #if golclub.rect.x >= SCREEN_WIDTH/2-150 and golclub.rect.right <= SCREEN_WIDTH/2+150:
                screen.blit(golclub.image, (golclub.rect.x,golclub.rect.y))
                golclub.move(5)
                if round >= 2:
                    #if golclub2.rect.x >= SCREEN_WIDTH/2-150 and golclub2.rect.right <= SCREEN_WIDTH/2+150:
                    screen.blit(golclub2.image, (golclub2.rect.x,golclub2.rect.y))
                    golclub2.move(-5)
                if round >= 3:
                    #if golclub3.rect.x >= SCREEN_WIDTH/2-150 and golclub3.rect.right <= SCREEN_WIDTH/2+150:
                    screen.blit(golclub3.image, (golclub3.rect.x,golclub3.rect.y))
                    golclub3.move(5)
                if round >= 4:
                    #if golclub4.rect.x >= SCREEN_WIDTH/2-150 and golclub4.rect.right <= SCREEN_WIDTH/2+150:
                    screen.blit(golclub4.image, (golclub4.rect.x,golclub4.rect.y))
                    golclub4.move(-5)
                if utheart.rect.colliderect(golclub.rect) or utheart.rect.colliderect(golclub2.rect) or utheart.rect.colliderect(golclub3.rect) or utheart.rect.colliderect(golclub4.rect):
                    sound_effects_channel.stop()
                    sound_effects_channel.play(vine_boom_sound)
                    player.health -= 2
                    if player.health == 0:
                        gamestate = "gameover"
                        last = pygame.time.get_ticks()
                        continue
                    golclub.rect.left = leftmostbox-200
                    golclub.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))
                    golclub2.rect.right = rightmostbox+200
                    golclub2.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))
                    golclub3.rect.top = upmostbox-200
                    golclub3.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))
                    golclub4.rect.bottom = downmostbox+200
                    golclub4.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))

            if golclub.rect.right >= rightmostbox+200:
                golclub.rect.left = leftmostbox-200
                golclub.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))

            if golclub2.rect.left <= leftmostbox-200:
                golclub2.rect.right = rightmostbox+200
                golclub2.rect.bottom = random.randint(int(SCREEN_HEIGHT/2-112.5),int(SCREEN_HEIGHT/2+150))

            if golclub3.rect.bottom >= downmostbox+200:
                golclub3.rect.top = upmostbox-200
                golclub3.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))

            if golclub4.rect.top <= upmostbox-200:
                golclub4.rect.bottom = downmostbox+200
                golclub4.rect.right = random.randint(int(SCREEN_WIDTH/2-112.5),int(SCREEN_WIDTH/2+150))

            screen.blit(utheart.image, (utheart.rect.x, utheart.rect.y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            key = pygame.key.get_pressed()
            
            if key[pygame.K_UP]:
                utheart.rect.y -= 6
            if key[pygame.K_DOWN]:
                utheart.rect.y += 6
            if key[pygame.K_LEFT]:
                utheart.rect.x -= 6
            if key[pygame.K_RIGHT]:
                utheart.rect.x += 6
            
            pygame.display.flip()

            clock.tick(60)

            now = pygame.time.get_ticks()

    elif gamestate == "shop":

        myman=0

        myfont = pygame.font.SysFont("Arial", 30)

        mouse = pygame.mouse.get_pos()

        screen.fill("black")

        thisfont = pygame.font.SysFont("Arial", 30)

        thistxt = "Coins: " + str(gamestats["money"])

        mytxt = thisfont.render(thistxt, True, "white")

        screen.blit(mytxt, (10,10))

        screen.blit(truesans, (trrect.x,trrect.y-300))

        blackx = SCREEN_WIDTH/2-390
        blacky = SCREEN_HEIGHT-640

        returnbutton.rect.x = blackx
        returnbutton.rect.y = blacky+254

        pygame.draw.rect(screen, "white", (SCREEN_WIDTH/2-400,SCREEN_HEIGHT-650,800,300))
        pygame.draw.rect(screen, "black", (blackx,blacky,780,280))
        screen.blit(returnbutton.image, (returnbutton.rect.x,returnbutton.rect.y))

        myrects = []
        mifontes = []

        for item in inshop:
            thistext = {"text":myfont.render((inshop.get(item))[0]+" - " + str((inshop.get(item))[2]) + " Coins - +" + str((inshop.get(item))[1]) + " HP", True, (255,255,255)),"rect":0}
            tsrectt = thistext["text"].get_rect()
            tsrectt.x = blackx
            tsrectt.y = blacky+myman
            thistext["rect"] = tsrectt
            myrects.append(tsrectt)
            mifontes.append(thistext)
            screen.blit(thistext["text"], (thistext["rect"].x, thistext["rect"].y))
            myman+=tsrectt.h+10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if returnbutton.rect.collidepoint(mouse):
                    gamestate="main"
                    last = pygame.time.get_ticks()
                    continue
                for i in myrects:
                    if i.collidepoint(mouse):
                        for z in mifontes:
                            if z["rect"].x == i.x and z["rect"].y == i.y:
                                if gamestats["money"] >= list(inshop.values())[mifontes.index(z)][2]:
                                    gamestats["money"] -= list(inshop.values())[mifontes.index(z)][2]
                                    playerinv[len(playerinv)] = list(inshop.values())[mifontes.index(z)]
                                    inshop.pop(list(inshop.keys())[mifontes.index(z)])

        pygame.display.flip()

        clock.tick(60)

        now = pygame.time.get_ticks()
    
    elif gamestate == "gameover":
        if current_music != "gameover":
            if pygame.mixer.music.get_busy():  # Check if music is currently playing
                pygame.mixer.music.fadeout(500)  # Fade out the current music over 500ms
            pygame.mixer.music.load(music_files["gameover"])  # Load the fight music
            pygame.mixer.music.play(-1)  # Play the fight music in a loop
            current_music = "gameover"
        screen.fill("black")

        screen.fill((0,0,0))
        pygame.draw.rect(screen, "black", (SCREEN_WIDTH/2-400,SCREEN_HEIGHT/2-200,800,400))
        screen.blit(gameover, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

        if now-last >= 15000:
            running = False
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        pygame.display.flip()
        clock.tick(60)
        now = pygame.time.get_ticks()
    elif gamestate == "wingame":
        if current_music != "gameover":
            if pygame.mixer.music.get_busy():  # Check if music is currently playing
                pygame.mixer.music.fadeout(500)  # Fade out the current music over 500ms
            pygame.mixer.music.load(music_files["gameover"])  # Load the fight music
            pygame.mixer.music.play(-1)  # Play the fight music in a loop
            current_music = "gameover"
        screen.fill("black")

        screen.fill((0,0,0))
        pygame.draw.rect(screen, "black", (SCREEN_WIDTH/2-400,SCREEN_HEIGHT/2-200,800,400))
        screen.blit(wingame, (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

        if now-last >= 15000:
            running = False
            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        pygame.display.flip()
        clock.tick(60)
        now = pygame.time.get_ticks()
pygame.quit()
