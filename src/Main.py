import pygame
from WorldGenerator import WorldGenerator
from Tiles import Tiles
from Config import *
from Warrior import Warrior

tileset = pygame.image.load("./data/tileset.png").convert_alpha()
tileset = pygame.transform.scale(tileset, (tileset.get_width() * 2, tileset.get_height() * 2))

tiles = Tiles(tileset, tile_width, tile_height)
clock = pygame.time.Clock()

world = WorldGenerator()

def show_grid():
    for x in range(0, window_width, tile_height):
        pygame.draw.line(screen, grid_color, (x, 0), (x, window_height))
        for y in range(0, window_height, tile_width):
            pygame.draw.line(screen, grid_color, (0, y), (window_width, y))

# GAME LOOP
last_frame_time = pygame.time.get_ticks()

warrior_list = []
for w in range(70):
    warrior_list.append(Warrior(64, 200))
start_time = pygame.time.get_ticks()
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        for w in warrior_list:
            w.jump()
    
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {round(fps)}", True, text_color, bg_color)

    delta_time = (pygame.time.get_ticks() - last_frame_time) / 1000

    temp_surface.fill(bg_color)
    world.update_objects(delta_time)
    for w in warrior_list:
        w.on_ground = False

    for obj in world.world_objects:
        if window_width > obj["pos_x"]:
            temp_surface.blit(tiles.all[obj["type_id"]], (obj["pos_x"], obj["pos_y"]))
            
            for warrior in warrior_list:
                if warrior.right_collide(pygame.Rect(obj["pos_x"], obj["pos_y"], 64, 64)):
                    if obj["type"]=="obstacle":
                        warrior_list.remove(warrior)
                    
                
                if warrior.bottom_collide(pygame.Rect(obj["pos_x"], obj["pos_y"], 64, 64)) and obj["type"]=="ground":
                    # Adjust the warrior's position and velocity based on the collision
                    if warrior.velocity > 0:
                        # Falling down
                        warrior.set_on_ground(obj["pos_y"])
                    elif warrior.velocity < 0:
                        # Jumping up, adjust position only if necessary
                        if warrior.rect.bottom <= obj["pos_y"]:
                            warrior.rect.bottom = obj["pos_y"]-2
                            warrior.velocity = 0
            

    
    
    for warrior in warrior_list:
        warrior.update(delta_time)
        temp_surface.blit(warrior.image , (warrior.rect.x, warrior.rect.y))
        #pygame.draw.rect(temp_surface, (0,255,0), warrior.bottom_rect)
        #pygame.draw.rect(temp_surface, (0,0,255), warrior.right_rect)
    
    
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_text = font.render(f"Time: {round(elapsed_time)}s", True, text_color, bg_color)
    temp_surface.blit(time_text, text_position)

    world.increment_speed(elapsed_time)
    

    screen.blit(temp_surface, (0, 0))
    #show_grid()
    pygame.display.flip()

    last_frame_time = pygame.time.get_ticks()
    clock.tick(60)
