import pygame
import neat
import time
import os
import random

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")))
               ]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count**2

        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            d -= 2
        
        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt = max(self.tilt - self.ROT_VEL, -90)

    def draw(self, win):
        self.img_count += 1
        
        self.current_image_index = int(self.img_count / self.ANIMATION_TIME % len(self.IMGS))
        self.img = self.IMGS[self.current_image_index]

        if self.img_count > self.ANIMATION_TIME * len(self.IMGS):
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

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