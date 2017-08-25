import pygame
import sys
from pygame.locals import*


def main():
    pygame.init()
    window_size = Rect(0, 0, 800, 600)
    screen = pygame.display.set_mode(window_size.size)
    surface = pygame.Surface((75, 25))
    surface.fill((255, 255, 0))
    rect = surface.get_rect()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    sys.exit()
            elif event.type == QUIT:
                running = False
                sys.exit()

        cur_speed = control(event)

        rect = rect.move(cur_speed).clamp(window_size)
        screen.blit(surface, rect)
        pygame.display.update()


def control(event):
    speed = [x, y] = [0, 0]
    speed_offset = 10
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            speed[0] -= speed_offset
        if event.key == pygame.K_RIGHT:
            speed[0] = speed_offset
        if event.key == pygame.K_UP:
            speed[1] -= speed_offset
        if event.key == pygame.K_DOWN:
            speed[1] = speed_offset
    if event.type in (pygame.KEYUP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN):
        speed = [0, 0]
    return speed


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect()

if __name__ == '__main__':
    main()
