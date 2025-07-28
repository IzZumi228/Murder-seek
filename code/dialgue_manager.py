import pygame
from settings import *

class DialogueManager:
    def __init__(self):
        self.active = False
        self.text = ""
        self.font = pygame.font.Font(None, 26)
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.padding = 20
        
        self.options = []
        self.option_rects = []
        self.button_color = (50, 50, 50)
        self.button_hover = (80, 80, 80)
        
        # click handling
        self.mouse_was_pressed = False
    
    def open(self, text):
        self.active = True
        self.text = text
    
    def close(self):
        self.active = False
        self.text = ""
    
    def set_options(self, options):  # list of (label, response_text)
        self.options = options
    
    def clear_options(self):
        self.options = []
        self.option_rects = []
    
    def handle_click(self, mouse_pos, mouse_pressed, option_rects):
        """Handle mouse clicks - call this from your main game loop"""
        clicked = False
        chosen_label = None
        if mouse_pressed:
            for rect, label, response_text in option_rects:
                if rect.collidepoint(mouse_pos):
                    self.open(response_text)
                    clicked = True
                    chosen_label = label
                    break
        
        self.mouse_was_pressed = mouse_pressed
        return clicked, chosen_label
    
    def draw(self, surface):
        self.option_rects = []  # clear old option rects
    
        # constants for layout
        option_button_height = self.font.get_height() + self.padding
        option_area_height = (option_button_height + 10) * len(self.options)  # total height for all option buttons
        reserved_space_below = option_area_height + 40  # space below dialogue box for options + padding
    
        if self.active:
            # word wrap the dialogue text
            max_text_width = SCREEN_WIDTH - 2 * self.padding
            words = self.text.split(' ')
            lines = []
            current_line = ""
    
            for word in words:
                test_line = current_line + word + " "
                test_surf = self.font.render(test_line, True, self.text_color)
                if test_surf.get_width() <= max_text_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)
    
            # render dialogue box
            line_height = self.font.get_height()
            total_height = line_height * len(lines)
            box_width = max_text_width + self.padding * 2
            box_height = total_height + self.padding * 2
            bg_rect = pygame.Rect(0, 0, box_width, box_height)
    
            # position above the option area
            bg_rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - reserved_space_below)
    
            pygame.draw.rect(surface, self.bg_color, bg_rect)
            for i, line in enumerate(lines):
                text_surf = self.font.render(line, True, self.text_color)
                text_rect = text_surf.get_rect()
                text_rect.topleft = (bg_rect.left + self.padding, bg_rect.top + self.padding + i * line_height)
                surface.blit(text_surf, text_rect)
    
        # draw options 
        if self.options:
            button_y = SCREEN_HEIGHT - option_area_height  # align top of first button
            for i, (label, response_text) in enumerate(self.options):
                text_surf = self.font.render(label, True, self.text_color)
                text_rect = text_surf.get_rect()
                button_width = text_rect.width + self.padding * 2
                button_height = text_rect.height + self.padding
                button_x = SCREEN_WIDTH // 2 - button_width // 2
    
                current_button_y = button_y + i * (button_height + 10)
                button_rect = pygame.Rect(button_x, current_button_y, button_width, button_height)
    
                # Hover effect
                mouse_pos = pygame.mouse.get_pos()
                color = self.button_hover if button_rect.collidepoint(mouse_pos) else self.button_color
                pygame.draw.rect(surface, color, button_rect, border_radius=8)
                surface.blit(text_surf, text_surf.get_rect(center=button_rect.center))
    
                self.option_rects.append((button_rect, label, response_text))
    