import pygame
import random
import textwrap
from pytmx import *
from pygame_aseprite_animation import *
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

sprite_group = pygame.sprite.Group()