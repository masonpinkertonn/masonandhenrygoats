import pygame, sys, math
from random import randint

image_cache={}

class Wizard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 15
        self.sprites = []
        names = []
        for i in range(4):
            names.append('wiz00'+str(i)+'.png')
        for i in names:
            tempimg = pygame.image.load(i)
            tempimg = pygame.transform.scale(tempimg, (200,200))
            self.sprites.append(tempimg)
        self.currentsprite = 0
        self.image = self.sprites[self.currentsprite]
        self.rect = self.image.get_rect()
        self.isdefeated = False
    def idleanimation(self):
        self.currentsprite += 0.1

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0

        self.image = self.sprites[int(self.currentsprite)]

class PSHOOTER(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 15
        self.sprites = []
        names = []
        for i in range(4):
            names.append('plant00'+str(i)+'.png')
        for i in names:
            tempimg = pygame.image.load(i)
            tempimg = pygame.transform.scale(tempimg, (200,200))
            self.sprites.append(tempimg)
        self.currentsprite = 0
        self.image = self.sprites[self.currentsprite]
        self.rect = self.image.get_rect()
        self.isdefeated = False
    def idleanimation(self):
        self.currentsprite += 0.1

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0

        self.image = self.sprites[int(self.currentsprite)]

def load_image(filename, scale=None):
    if filename not in image_cache:
        print(f"Loading image: {filename}")
        image = pygame.image.load(filename)
        if scale:
            image = pygame.transform.scale(image, scale)
        image_cache[filename] = image
    return image_cache[filename]

class NPC(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class sanbutton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("SANS.png", (225, 300))
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = -400
        self.isdefeated = False

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 15
        self.sprites = []
        names = []
        for i in range(4):
            names.append('birdie00'+str(i)+'.png')
        for i in names:
            tempimg = pygame.image.load(i)
            tempimg = pygame.transform.scale(tempimg, (200,200))
            self.sprites.append(tempimg)
        self.currentsprite = 0
        self.image = self.sprites[self.currentsprite]
        self.rect = self.image.get_rect()
        self.isdefeated = False
    def idleanimation(self):
        self.currentsprite += 0.1

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0

        self.image = self.sprites[int(self.currentsprite)]

class Golem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 15
        self.sprites = []
        names = []
        for i in range(10):
            names.append('Golem_01_Idle Blinking_00'+str(i)+'.png')
        names.append('Golem_01_Idle Blinking_010.png')
        names.append('Golem_01_Idle Blinking_011.png')
        for i in names:
            tempimg = pygame.image.load(i)
            tempimg = tempimg
            tempimg = pygame.transform.scale(tempimg, (200,200))
            self.sprites.append(tempimg)
        self.currentsprite = 0
        self.image = self.sprites[self.currentsprite]
        self.rect = self.image.get_rect()
        self.isdefeated = False
    def idleanimation(self):
        self.currentsprite += 0.1

        if self.currentsprite >= len(self.sprites):
            self.currentsprite = 0

        self.image = self.sprites[int(self.currentsprite)]

class CameraGroup(pygame.sprite.Group):
    def __init__(self, tmx_data):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Box setup
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # TMX data
        self.tmx_data = tmx_data
        

        # Tilemap offset
        self.tilemap_offset_x = 0 #-2304 big map's values # Horizontal offset
        self.tilemap_offset_y = 0 #-4736 big map's values  # Vertical offset


    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self, player, mypeeps, e_button):
        # Update camera offset based on player position

        expansion = player.rect.inflate(50,50)

        self.box_target_camera(player)

        # Clear the screen
        self.display_surface.fill((0, 0, 0))

        # Draw TMX layers
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (
                        x * self.tmx_data.tilewidth - self.offset.x + self.tilemap_offset_x,
                        y * self.tmx_data.tileheight - self.offset.y + self.tilemap_offset_y
                    )
                    self.display_surface.blit(surf, pos)

        # Draw sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if isinstance(sprite, Golem):  # Check if the sprite is an NPC
                # Draw NPCs at their absolute positions
                if not(player.isgolemdefeated):
                    self.display_surface.blit(sprite.image, sprite.rect.topleft-self.offset)
            elif isinstance(sprite, Bird):  # Check if the sprite is an NPC
                # Draw NPCs at their absolute positions
                if not(player.isbirddefeated):
                    self.display_surface.blit(sprite.image, sprite.rect.topleft-self.offset)
            elif isinstance(sprite, PSHOOTER):  # Check if the sprite is an NPC
                # Draw NPCs at their absolute positions
                if not(player.isplantdefeated):
                    self.display_surface.blit(sprite.image, sprite.rect.topleft-self.offset)
            elif isinstance(sprite, Wizard):  # Check if the sprite is an NPC
                # Draw NPCs at their absolute positions
                if not(player.iswizdefeated):
                    self.display_surface.blit(sprite.image, sprite.rect.topleft-self.offset)
            else:
                # Draw other sprites with the camera offset
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

        for i in mypeeps:
            if not(i.isdefeated):
                if expansion.colliderect(i.rect):
                    self.display_surface.blit(e_button.image, (i.rect.center[0]-e_button.rect.w/2-self.offset[0],i.rect.center[1]-100-self.offset[1]))
                if player.rect.colliderect(i.rect):
                    player.docollisions(i.rect)