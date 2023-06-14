import neat, pickle
from Config import *

def run(config_path,train_func):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    
    p = neat.Population(config)

    p.add_reporter(neat.Checkpointer(50, filename_prefix='neat-checkpoint-'))
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(train_func,6000)
    with open('winner.pickle', 'wb') as f:
        print(winner)
        pickle.dump(winner, f)

def load_checkpoint(config_path, checkpoint_dir, train_func):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Create a checkpointer object
    checkpointer = neat.Checkpointer()

    # Load the checkpoint file
    checkpoint_file = checkpoint_dir
    # Replace 'X' with the generation number or checkpoint file you want to load

    population = checkpointer.restore_checkpoint(checkpoint_file)

    # Continue the evolution process
    population.run(train_func, 50)

def load_winner(winner_path, config_path, train_func):
    with open(winner_path, 'rb') as f:
        winner = pickle.load(f)

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                               neat.DefaultSpeciesSet, neat.DefaultStagnation,
                               config_path)

    genomes = [(1, winner)]

    # Run the training function with the loaded winner
    train_func(genomes, config)


def get_parameters(r, y, h, w, velocity):
    r.append(y)
    r.append(velocity)
    r.append(h)
    r.append(w)
    return tuple(r)