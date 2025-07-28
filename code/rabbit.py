import pygame
import os
from settings import *
from support import *
import random

class Rabbit(pygame.sprite.Sprite):
    def __init__(self, pos, boundary, group, z=LAYERS['overlays']):
        super().__init__(group)
        
        self.import_assets()
        
        self.timer = 0
        self.move_duration = random.uniform(1, 3)
        self.idle_duration = random.uniform(2, 4)
        self.direction = pygame.math.Vector2()
        self.status = 'right_idle'
        self.state = 'idle'  
        self.frame_index = 0
        
        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        
        # movement attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 100
        
      
        self.boundary_rect = pygame.Rect(boundary)
    
    def import_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
        }
        
        base_dir = os.path.dirname(os.path.abspath(__file__))  
        graphics_dir = os.path.join(base_dir, '..', 'graphics', 'animals', 'rabbit')
        
        for animation in self.animations.keys():
            full_path = os.path.join(graphics_dir, animation)
            self.animations[animation] = import_folder(full_path)
    
    def animate(self, dt):
        self.frame_index += 8 * dt
        
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        
        self.image = self.animations[self.status][int(self.frame_index)]
    
    def pick_direction(self):
        directions = [
            pygame.math.Vector2(0, -1),  # up
            pygame.math.Vector2(0, 1),   # down
            pygame.math.Vector2(1, 0),   # right
            pygame.math.Vector2(-1, 0),  # left
            pygame.math.Vector2(0, 0)    # small chance to stand still
        ]
        self.direction = random.choice(directions)
        
        # update status based on direction
        if self.direction.x > 0:
            self.status = 'right'
        elif self.direction.x < 0:
            self.status = 'left'
        elif self.direction.y > 0:
            self.status = 'down'
        elif self.direction.y < 0:
            self.status = 'up'
    
    def update_status(self):
        """Update animation status based on state and direction"""
        if self.state == 'idle':
            if self.direction.x > 0 or (self.direction.x == 0 and 'right' in self.status):
                self.status = 'right_idle'
            elif self.direction.x < 0 or (self.direction.x == 0 and 'left' in self.status):
                self.status = 'left_idle'
            elif self.direction.y > 0 or (self.direction.y == 0 and 'down' in self.status):
                self.status = 'down_idle'
            elif self.direction.y < 0 or (self.direction.y == 0 and 'up' in self.status):
                self.status = 'up_idle'
        else:  # moving
            if self.direction.x > 0:
                self.status = 'right'
            elif self.direction.x < 0:
                self.status = 'left'
            elif self.direction.y > 0:
                self.status = 'down'
            elif self.direction.y < 0:
                self.status = 'up'
    
    def move(self, dt):
        # try moving in the current direction
        move_vector = self.direction * self.speed * dt
        new_pos = self.pos + move_vector
        new_rect = self.rect.copy()
        new_rect.center = new_pos
        
        # only move if still within boundary
        if self.boundary_rect.collidepoint(new_rect.center):
            self.pos = new_pos
            self.rect.center = self.pos
        else:
            self.direction = pygame.math.Vector2()
            self.state = 'idle'
            self.timer = 0
    
    def update(self, dt):
        self.timer += dt
        
        if self.state == 'idle':
            if self.timer >= self.idle_duration:
                self.timer = 0
                self.state = 'move'
                self.pick_direction()
                self.move_duration = random.uniform(1, 3)
        elif self.state == 'move':
            if self.timer >= self.move_duration:
                self.timer = 0
                self.state = 'idle'
                self.direction = pygame.math.Vector2()
                self.idle_duration = random.uniform(2, 4)
            else:
                self.move(dt)
        
     
        self.update_status()
        self.animate(dt)