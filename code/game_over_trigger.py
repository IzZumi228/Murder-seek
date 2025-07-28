import pygame
from settings import *

class FinishingTrigger(pygame.sprite.Sprite):
    def __init__(self, pos, groups, z=LAYERS['overlays']):
        super().__init__(groups)

        self.z = z
        
        self.image = pygame.Surface((120,250), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        

