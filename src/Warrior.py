import pygame, math
from pygame.locals import *

class Warrior(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.height = 128
        self.width = 64
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))  # Red rectangle for visualization
        self.rect = pygame.Rect(x, y, 64, 128)
        self.rect.x = x
        self.rect.y = y

        self.bottom_rect = pygame.Rect(x, y+118, 64, 10)
        self.bottom_rect.x = x
        self.bottom_rect.y = y+118

        self.right_rect = pygame.Rect(x+60, y, 64, 108)
        self.right_rect.x = x
        self.right_rect.y = y

        self.velocity = 0
        self.jump_power = -1400
        self.gravity = 60
        self.on_ground = False

    def update(self, delta_time):
        self.gravity_effect()
        self.move_warrior(math.ceil(self.velocity * delta_time))

    def move_warrior(self,y):
        self.rect.y+=y
        self.bottom_rect.y+=y
        self.right_rect.y+=y

    def gravity_effect(self):
        if self.on_ground and self.velocity >= 0:
            self.velocity = 0
        else:
            self.velocity += self.gravity

    def set_on_ground(self, y):
        if self.on_ground:
            return 
        self.on_ground = True
        self.rect.y = y-self.height
        self.bottom_rect.y = y-10
        self.right_rect.y = y-self.height


    def jump(self):
        if self.on_ground:
            self.velocity += self.jump_power
            self.on_ground=False

    def right_collide(self, sprite):
        return self.right_rect.colliderect(sprite)
    
    def bottom_collide(self, sprite):
        return self.bottom_rect.colliderect(sprite)
    

