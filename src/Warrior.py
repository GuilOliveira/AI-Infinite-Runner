import pygame
import math

class Warrior(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.height = 128
        self.width = 64

        self.run_frames = []
        self.jump_frames = []
        self.fall_frames = []
        self.current_frame = 0  # Current frame index
        self.animation_speed = 0.05  # Animation speed (in seconds)
        self.last_update = pygame.time.get_ticks()
        self.animation_stage = "fall"

        self.load_frames()
        self.image = self.fall_frames[0]
        self.rect = self.image.get_rect()
        
        self.rect.x = x-12
        self.rect.y = y
        self.last_y = y

        self.bottom_rect = pygame.Rect(x, y+118, 64, 10)
        self.bottom_rect.x = x
        self.bottom_rect.y = y+102.40

        self.right_rect = pygame.Rect(x+60, y+20, 64, 102.40)
        self.right_rect.x = x
        self.right_rect.y = y+12

        self.velocity = 0
        self.jump_power = -1400
        self.gravity = 60
        self.on_ground = False
    
    def load_frames(self):
        run_frames = pygame.image.load("../data/_Run.png").convert_alpha()
        self.run_frames = self.set_frames(10, run_frames)

        fall_frames = pygame.image.load("../data/_Fall.png").convert_alpha()
        self.fall_frames = self.set_frames(3, fall_frames)

        jump_frames = pygame.image.load("../data/_Jump.png").convert_alpha()
        self.jump_frames = self.set_frames(3, jump_frames)

    def set_frames(self, n, frames, base_width=40):
        all_frames = []
        frame_height = frames.get_height()
        for n in range(0, n):
            frame = frames.subsurface(n * 32 + base_width * (1+n*2)+8*n, frame_height/2, 32, 40)
            frame = pygame.transform.scale(frame, (frame.get_width()*3.2, frame.get_height()*3.2))
            all_frames.append(frame)
        return all_frames


    def update(self, delta_time):
        self.gravity_effect()
        self.move_warrior(math.ceil(self.velocity * delta_time))
        self.animate()
        

    def animate(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_update
        old = self.animation_stage
        current_set = []

        if (self.velocity>=-70 and self.velocity<=70) or self.on_ground:
            self.animation_stage="run"
            current_set = self.run_frames

        elif self.velocity<0 and self.on_ground==False:
            self.animation_stage="fall"
            current_set = self.jump_frames
        
        elif self.velocity>0 and self.on_ground==False:
            self.animation_stage="jump"
            current_set = self.fall_frames

        

        if elapsed_time >= self.animation_speed * 1000:
            if old != self.animation_stage or len(current_set)-1<=self.current_frame:
                self.current_frame = 0
            else:
                self.current_frame+=1
            self.image = current_set[self.current_frame]
            self.last_update = current_time
        self.last_y=self.rect.y

    def move_warrior(self, y):
        self.rect.y += y
        self.bottom_rect.y += y
        self.right_rect.y += y

    def gravity_effect(self):
        if (self.on_ground and self.velocity >= 0):
            self.velocity = 0
        else:
            self.velocity += self.gravity

    def set_on_ground(self, y):
        if self.on_ground:
            return 
        self.velocity = 0
        self.on_ground = True
        self.rect.y = y - self.height
        self.bottom_rect.y = y - 10
        self.right_rect.y = y - self.height + 12

    def jump(self, pop):
        if self.on_ground:
            self.velocity += self.jump_power-pop*2.4
            self.on_ground = False

    def right_collide(self, sprite):
        return self.right_rect.colliderect(sprite)
    
    def bottom_collide(self, sprite):
        return self.bottom_rect.colliderect(sprite)
