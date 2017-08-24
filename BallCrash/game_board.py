import pygame
from sys import exit
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 800))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()