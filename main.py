import pygame
import neat
import os

from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(win, birds, pipes, base, score):
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    
    win.blit(BG_IMG, (0,0))
    
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    
    for bird in birds:
        bird.draw(win)

    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()

def main(genomes, config):
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    
    nets = []
    genome_list = []
    birds = []

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        genome.fitness = 0
        genome_list.append(genome)
    
    base = Base(730)
    pipes = [Pipe(WIN_WIDTH)]
    clock = pygame.time.Clock()

    score = 0
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            genome_list[x].fitness += 0.1
            
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] >= 0.5:
                bird.jump()

        add_pipe = False
        pipes_to_remove = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    genome_list[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    genome_list.pop(x)
            
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x+pipe.PIPE_TOP.get_width() < 0:
                pipes_to_remove.append(pipe)
            
            pipe.move()

        if add_pipe:
            score += 1
            for genome in genome_list:
                genome.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for pipe in pipes_to_remove:
            pipes.remove(pipe)
        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                genome_list.pop(x)
                
        base.move()
        draw_window(win, birds, pipes, base, score)   

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)
    
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main,50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)