import pygame

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
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
            tempimg = pygame.transform.scale(tempimg, (103.5,149))
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

class Golem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        names = []
        for i in range(10):
            names.append('Golem_01_Idle Blinking_00'+str(i)+'.png')
        names.append('Golem_01_Idle Blinking_010.png')
        names.append('Golem_01_Idle Blinking_011.png')
        for i in names:
            tempimg = pygame.image.load(i)
            tempimg = pygame.transform.scale(tempimg, (200,200))
            self.sprites.append(tempimg)
        self.currentsprite = 0
        self.image = self.sprites[self.currentsprite]
        self.rect = self.image.get_rect()
    def idleanimation(self):
        self.currentsprite += 0.1

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0

        self.image = self.sprites[int(self.currentsprite)]

def golemdialogue(currentline):
    dialogue = open('golemtext.npc', 'r')
    lines = []
    for line in dialogue:
        if '\n' in line:
            line = line[0:-1]
        lines.append(line)
    dialogue.close()
    try:
        return (pygame.font.SysFont("Arial", 30).render(lines[currentline], True, (255,255,255)), currentline)
    except IndexError:
        currentline = 0
        return (pygame.font.SysFont("Arial", 30).render(lines[currentline], True, (255,255,255)), currentline)

running = True
clock = pygame.time.Clock()

player = Player()
golem = Golem()

dialogueline = 0

last = pygame.time.get_ticks()
now = pygame.time.get_ticks()

class ebutton:
    def __init__(self):
        self.image = pygame.image.load('e_button.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.isshowing = False

e_button = ebutton()

golem.rect.y = 400

def docollisions():
    if player.goingleft:
        player.rect.left = golem.rect.right#-1
    elif player.goingdown:
        player.rect.bottom = golem.rect.top#+1
    elif player.goingup:
        player.rect.top = golem.rect.bottom#-1
    elif player.goingright:
        player.rect.right = golem.rect.left#+1

while running:
    screen.fill((0,0,0))

    pygame.draw.rect(screen, (255,255,255), (player.rect.x, player.rect.y, player.rect.w, player.rect.h))

    x = golemdialogue(dialogueline)

    dialogueline = x[1]

    screen.blit(player.image, (player.rect.x, player.rect.y))

    if player.rect.x >= SCREEN_WIDTH-305:
        player.rect.x = SCREEN_WIDTH-305
    if player.rect.x <= 0:
        player.rect.x = 0
    if player.rect.y <= 0:
        player.rect.y = 0
    if player.rect.y >= SCREEN_HEIGHT-185:
        player.rect.y = SCREEN_HEIGHT-185

    golem.idleanimation()

    screen.blit(golem.image, (golem.rect.x, golem.rect.y))

    expansion = player.rect.inflate(50,50)

    if expansion.colliderect(golem.rect):
        screen.blit(e_button.image, (golem.rect.x+50,golem.rect.y-60))
        screen.blit(x[0], (600,600))
        e_button.isshowing = True
    else:
        e_button.isshowing = False
        dialogueline = 0

    if player.rect.colliderect(golem.rect):
        docollisions()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            player.ismoving = False
            player.goingup = False
            player.goingdown = False
            player.goingleft = False
            player.goingright = False

    key = pygame.key.get_pressed()
    
    if key[pygame.K_UP]:
        player.goingup = True
        player.rect.y -= 5
        player.movement()
    elif key[pygame.K_DOWN]:
        player.goingdown = True
        player.rect.y += 5
        player.movement()
    elif key[pygame.K_LEFT]:
        player.goingleft = True
        player.rect.x -= 5
        player.isleft = True
        player.movement()
    elif key[pygame.K_RIGHT]:
        player.goingright = True
        player.rect.x += 5
        player.isleft = False
        player.movement()
    if not(player.ismoving):
        player.idleanimation()
    if key[pygame.K_e] and e_button.isshowing:
        if now - last >= 1500:
            last = pygame.time.get_ticks()
            dialogueline += 1

    pygame.display.flip()

    clock.tick(60)

    now = pygame.time.get_ticks()

pygame.quit()