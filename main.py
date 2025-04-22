import pygame

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class hitbutton:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

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
        if lines[currentline][0] == "-":
            templine = lines[currentline][1:]
            return (pygame.font.SysFont("Arial", 30).render(templine, True, (255,255,255)), currentline, "player")
        else:
            return (pygame.font.SysFont("Arial", 30).render(lines[currentline], True, (255,255,255)), currentline, "monster")
    except IndexError:
        currentline = 0
        if lines[currentline][0] == "-":
            templine = lines[currentline][1:]
            return (pygame.font.SysFont("Arial", 30).render(templine, True, (255,255,255)), currentline, "player")
        else:
            return (pygame.font.SysFont("Arial", 30).render(lines[currentline], True, (255,255,255)), currentline, "monster")

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

gamestate = "main"

fightbutton = pygame.image.load('FIGHTBUTTON.png')
fightbuttonrect = fightbutton.get_rect()

rollx = 20
tempx = 20
linegoinleft = False
linestopped = False

hb1 = hitbutton("red", rollx, 100, 150, 100)
hb2 = hitbutton("yellow", rollx+150, 100, 100, 100)
hb3 = hitbutton("green", rollx+250, 100, 50, 100)
hb4 = hitbutton("yellow", rollx+300, 100, 100, 100)
hb5 = hitbutton("red", rollx+400, 100, 150, 100)

hbrects = [hb1, hb2, hb3, hb4, hb5]

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Undertale.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()

class Weapon:
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

utheart = Heart()

golclub = Weapon('golemweapon.png')

while running:
    if gamestate == "main":
        screen.fill((0,0,0))

        #pygame.draw.rect(screen, (255,255,255), (player.rect.x, player.rect.y, player.rect.w, player.rect.h))

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
            if x[2] == "monster":
                screen.blit(x[0], (golem.rect.x+100,golem.rect.y-20))
            elif x[2] == "player":
                screen.blit(x[0], (player.rect.x,player.rect.y))
            e_button.isshowing = True
        else:
            e_button.isshowing = False
            dialogueline = 0

        if player.rect.colliderect(golem.rect):
            docollisions()

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
                if dialogueline == 5:
                    dialogueline = 0
                    gamestate = "fight"
                    continue
                dialogueline += 1

        pygame.display.flip()

        clock.tick(60)

        now = pygame.time.get_ticks()

    elif gamestate == "fight":
        screen.fill("red")

        screen.blit(fightbutton, (100,100))

        fightbuttonrect.x = 100
        fightbuttonrect.y = 100

        if now - last >= 3000:
            gamestate = "main"
            continue
        
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fightbuttonrect.collidepoint(mouse):
                    gamestate = "attack"
                    continue
        
        pygame.display.flip()

        clock.tick(60)

        now = pygame.time.get_ticks()

    elif gamestate == "attack":
        screen.fill((0,0,0))

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
                    hploss = 5
                elif thiscolor == "yellow":
                    hploss = 10
                elif thiscolor == "green":
                    hploss = 15
                gamestate = "defend"
                last = pygame.time.get_ticks()
                continue
                
        pygame.draw.rect(screen, hb1.color, (hb1.x, hb1.y, hb1.width, hb1.height))
        pygame.draw.rect(screen, hb2.color, (hb2.x, hb2.y, hb2.width, hb2.height))
        pygame.draw.rect(screen, hb3.color, (hb3.x, hb3.y, hb3.width, hb3.height))
        pygame.draw.rect(screen, hb4.color, (hb4.x, hb4.y, hb4.width, hb4.height))
        pygame.draw.rect(screen, hb5.color, (hb5.x, hb5.y, hb5.width, hb5.height))
        pygame.draw.line(screen, "white", (tempx,80), (tempx,220), 3)
        if tempx == 570 and not(linestopped):
            linegoinleft = True
        if tempx == 20 and not(linestopped):
            linegoinleft = False
        if linegoinleft and not(linestopped):
            tempx-=5
        elif not(linegoinleft) and not(linestopped):
            tempx+=5

        pygame.display.flip()

        clock.tick(60)

        now = pygame.time.get_ticks()

    elif gamestate == "defend":
        screen.fill((0,0,0))

        #pygame.draw.rect()

        if now-last >= 4000:
            screen.blit(golclub.image, (golclub.rect.x,golclub.rect.y))

        screen.blit(utheart.image, (utheart.rect.x, utheart.rect.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        key = pygame.key.get_pressed()
        
        if key[pygame.K_UP]:
            utheart.rect.y -= 5
        elif key[pygame.K_DOWN]:
            utheart.rect.y += 5
        elif key[pygame.K_LEFT]:
            utheart.rect.x -= 5
        elif key[pygame.K_RIGHT]:
            utheart.rect.x += 5
        
        pygame.display.flip()

        clock.tick(60)

        now = pygame.time.get_ticks()

pygame.quit()