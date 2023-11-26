import pygame
import neat
import time
import os

from bird import Bird
from pipe import Pipe
from base import Base

WIN_WIDTH = 550
WIN_HEIGHT = 800


BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    bird = Bird(200,200)
    
    clock = pygame.time.Clock()


    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)   

    pygame.quit()
    quit()

main()