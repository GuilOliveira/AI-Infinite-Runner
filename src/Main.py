import pygame
from WorldGenerator import WorldGenerator
from Tiles import Tiles
from Config import *

tileset = pygame.image.load("./data/tileset.png")
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {round(fps)}", True, text_color, bg_color)

    delta_time = (pygame.time.get_ticks() - last_frame_time) / 1000

    temp_surface.fill(bg_color)
    world.update_objects(delta_time)

    for obj in world.world_objects:
        if 0 <= obj["type_id"] < len(tiles.all):
            temp_surface.blit(tiles.all[obj["type_id"]], (obj["pos_x"], obj["pos_y"]))

    # show_grid()
    temp_surface.blit(fps_text, text_position)
    screen.blit(temp_surface, (0, 0))
    pygame.display.flip()

    last_frame_time = pygame.time.get_ticks()
    clock.tick(60)
