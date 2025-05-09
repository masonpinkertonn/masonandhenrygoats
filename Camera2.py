import pygame, sys, math
from random import randint

class NPC(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

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
        self.tilemap_offset_x = -2304  # Horizontal offset
        self.tilemap_offset_y = -4736   # Vertical offset


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

    def custom_draw(self, player):
        # Update camera offset based on player position
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
            if isinstance(sprite, NPC):  # Check if the sprite is an NPC
                # Draw NPCs at their absolute positions
                self.display_surface.blit(sprite.image, sprite.rect.topleft)
            else:
                # Draw other sprites with the camera offset
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)