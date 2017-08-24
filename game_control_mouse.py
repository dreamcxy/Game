import pygame
import sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 500))


pos_x = 300
pos_y = 460

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEMOTION:
            pos_x, pos_y = event.pos
    screen.fill((0, 0, 200))

    # move rectangleon the screen
    if pos_y < 0:
        pos_y = 0
    elif pos_y > 460:
        pos_y = 460
    if pos_x > 480:
        pos_x = 480
    elif pos_x < 0:
        pos_x = 0

    # draw the rectangle
    color = 255, 255, 0
    width = 0  # solid dill
    pos = pos_x, pos_y
    radius = 100

    pygame.draw.circle(screen, color, pos, radius	, width)

    # refresh
    pygame.display.update()
