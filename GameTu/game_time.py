import pygame
from pygame.locals import *
import time
import sys

pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 600))
pygame.display.set_caption("clock")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

DISPLAYSURF.fill(WHITE)
counts = 0

COUNT = pygame.USEREVENT + 1
pygame.time.set_timer(COUNT, 1000)


def showText(fontObj, text, x, y):
    textSurfaceObj = fontObj.render(text, True, GREEN, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

fontbigObj = pygame.font.Font("PAPYRUS.ttf", 48)
fontminObj = pygame.font.Font("PAPYRUS.ttf", 24)
showText(fontminObj, "Time: ", 100, 100)
showText(fontbigObj, "Count:", 100, 100)

while True:
    now = time.ctime()
    clock = now[11:19]
    showText(fontbigObj, clock, 200, 150)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == COUNT:
            counts = counts + 1
            countstext = str(counts)
            showText(fontbigObj, countstext, 200, 350)
    pygame.display.update()
