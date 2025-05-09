import pygame, sys
import random as randint
SCREEN_WIDTH = 1280 # compinf.current_w
SCREEN_HEIGHT = 720
class CameraGroup(pygame.sprite.Group):
    def __init__(self, tmx_data):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # TMX data
        self.tmx_data = tmx_data

        # Camera thresholds
        self.threshold_x = SCREEN_WIDTH // 4
        self.threshold_y = SCREEN_HEIGHT // 4

    def custom_draw(self, player):
        # Update camera offset based on player position and thresholds
        if player.rect.centerx > self.half_w + self.threshold_x:
            self.offset.x = player.rect.centerx - (self.half_w + self.threshold_x)
        elif player.rect.centerx < self.half_w - self.threshold_x:
            self.offset.x = player.rect.centerx - (self.half_w - self.threshold_x)

        if player.rect.centery > self.half_h + self.threshold_y:
            self.offset.y = player.rect.centery - (self.half_h + self.threshold_y)
        elif player.rect.centery < self.half_h - self.threshold_y:
            self.offset.y = player.rect.centery - (self.half_h - self.threshold_y)

        # Draw TMX layers
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * self.tmx_data.tilewidth - self.offset.x,
                           y * self.tmx_data.tileheight - self.offset.y)
                    self.display_surface.blit(surf, pos)

        # Draw sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)