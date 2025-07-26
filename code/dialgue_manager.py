import pygame
from settings import *

class DialogueManager:
    def __init__(self):
        self.active = False
        self.text = ""
        self.font = pygame.font.Font(None, 36)
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.padding = 20

    def open(self, text):
        self.active = True
        self.text = text

    def close(self):
        self.active = False

    def draw(self, surface):
        if self.active:
            text_surf = self.font.render(self.text, True, self.text_color)
            bg_rect = text_surf.get_rect(midbottom=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
            bg_rect.inflate_ip(self.padding * 2, self.padding * 2)
            pygame.draw.rect(surface, self.bg_color, bg_rect)
            surface.blit(text_surf, text_surf.get_rect(center=bg_rect.center))
