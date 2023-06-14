import pygame, neat
from WorldGenerator import WorldGenerator
from Tiles import Tiles
from Config import *
from Warrior import Warrior
from Neat_loads import *

tileset = pygame.image.load("../data/tileset.png").convert_alpha()
tileset = pygame.transform.scale(tileset, (tileset.get_width() * 2, tileset.get_height() * 2))

tiles = Tiles(tileset, tile_width, tile_height)
clock = pygame.time.Clock()

global gen
gen = 0 

def show_grid():
    for x in range(0, window_width, tile_height):
        pygame.draw.line(screen, grid_color, (x, 0), (x, window_height))
        for y in range(0, window_height, tile_width):
            pygame.draw.line(screen, grid_color, (0, y), (window_width, y))

def get_tile_values(objects):
    r = []
    
    ty=7
    for tx in range(1, 15):
        x = tx * 64
        y = ty * 64
        found = False
        for obj in objects:
            if (obj["pos_x"] >= x and obj["pos_x"] < x + 64) and (obj["pos_y"] >= y and obj["pos_y"] < y + 64):
                if obj["type"] == "ground":
                    r.append(1)
                    r.append(obj["pos_x"] / window_width)  # Normalize pos_x
                    r.append(obj["pos_y"] / window_height)
                    found = True
                    break  
                elif obj["type"] == "obstacle":
                    r.append(2)
                    r.append(obj["pos_x"] / window_width)  # Normalize pos_x
                    r.append(obj["pos_y"] / window_height)
                    found = True
                    break
        if not found:
            r.append(0)
            r.append(0)
            r.append(0)
            
    return r

def train(genomes, config):
    global gen
    gen+=1

    world = WorldGenerator()
    last_frame_time = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()

    generation_text = font.render(f"Generation: {gen}", True, text_color, bg_color)
    generation_position = (790, 10)
    population_position = (790, 32)
    

    nets = []
    warriors = []
    ge = []
    for genome_id, genome in genomes:
        
        genome.fitness = 0 
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        warriors.append(Warrior(64, 200))
        ge.append(genome)
        print(genome)

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if len(warriors)<=0:
            is_running=False

        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_SPACE]:
        #    for w in warrior_list:
        #        w.jump()
        

        delta_time = (pygame.time.get_ticks() - last_frame_time) / 1000
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        for x, warrior in enumerate(warriors):
            ge[x].fitness=elapsed_time
        
        world.update_objects(delta_time)
        for w in warriors:
            w.on_ground = False
        temp_surface.fill(bg_color)
        for obj in world.world_objects:
            if window_width > obj["pos_x"]:
                temp_surface.blit(tiles.all[obj["type_id"]], (obj["pos_x"], obj["pos_y"]))
                if obj["pos_x"]>=0 and obj["pos_x"]<=4*64:
                    for x, warrior in enumerate(warriors):
                        if warrior.right_collide(pygame.Rect(obj["pos_x"], obj["pos_y"], 64, 64)):
                            if obj["type"]=="obstacle":
                                ge[x].fitness *= 0.9
                                warriors.pop(x)
                                nets.pop(x)
                                ge.pop(x)
                            
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
                        else:
                            if warrior.rect.y>6*64:
                                warrior.set_on_ground(8*64)
                
        for x, warrior in enumerate(warriors):
            if warrior.rect.y>=7*64 and not warrior.on_ground :
                ge[x].fitness *= 0.7
                warriors.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        r=(get_tile_values(world.world_objects))
        for x, warrior in enumerate(warriors):
            ge[x].fitness+=elapsed_time*0.2
            output = nets[x].activate(get_parameters(r.copy(), warrior.right_rect.y, warrior.right_rect.y+102.40, 60, warrior.velocity))
            if output[0]>0.5:
                warrior.jump(len(warriors))
                ge[x].fitness-=1
        
        for warrior in warriors:
            warrior.update(delta_time)
            temp_surface.blit(warrior.image , (warrior.rect.x, warrior.rect.y))
            #pygame.draw.rect(temp_surface, (0,255,0), warrior.bottom_rect)
            #pygame.draw.rect(temp_surface, (0,0,255), warrior.right_rect)
        
        
        
        
        
        
        time_text = font.render(f"Time: {round(elapsed_time)}s", True, text_color, bg_color)
        population_text = font.render(f"Population: {len(warriors)}", True, text_color, bg_color)
        
        temp_surface.blit(time_text, text_position)
        temp_surface.blit(generation_text, generation_position)
        temp_surface.blit(population_text, population_position)     

        screen.blit(temp_surface, (0, 0))
        #show_grid()
        pygame.display.flip()

        last_frame_time = pygame.time.get_ticks()
        clock.tick(60)


load_winner(local_dir+"/winner.pickle",config_path, train)
#load_checkpoint(config_path, "neat-checkpoint-152", train)
#run(config_path, train)

