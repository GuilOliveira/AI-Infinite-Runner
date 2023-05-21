import pygame

window_width = 960
window_height = 576

pygame.init()

screen = pygame.display.set_mode((window_width, window_height))
temp_surface = pygame.Surface((window_width, window_height))
pygame.display.set_caption("IA")

font = pygame.font.Font(None, 28)
text_color = (255, 255, 255)  # White
text_position = (10, 10)  # Top-left corner of the window

bg_color = (50, 130, 255)
grid_color = (255, 255, 255)
tile_width = int(window_width / 15)
tile_height = int(window_height / 9)