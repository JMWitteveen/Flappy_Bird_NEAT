import pygame
import neat
import time
import os

from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(win, bird, pipes, base, score):
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    
    win.blit(BG_IMG, (0,0))
    
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    bird.draw(win)

    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(700)]
    clock = pygame.time.Clock()

    score = 0
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #bird.move()

        add_pipe = False
        pipes_to_remove = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            
            if pipe.x+pipe.PIPE_TOP.get_width() < 0:
                pipes_to_remove.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for _ in pipes_to_remove:
            pipes.remove(_)
        
        if bird.y + bird.img.get_height() >= 730:
            pass

        base.move()
        draw_window(win, bird, pipes, base, score)   

    pygame.quit()
    quit()

main()