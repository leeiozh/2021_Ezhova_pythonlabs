import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((600, 600))
screen.fill([215, 215, 225])
circle(screen, (0, 0, 0), (300,305), 133, 133)
circle(screen, (255, 255, 2), (300, 305), 132, 132)
circle(screen, (0, 0, 0), (250, 270), 26, 1)
circle(screen, (255, 0, 0), (250, 270), 25, 15)
circle(screen, (0, 0, 0), (250,270), 10, 10)
circle(screen, (0, 0, 0), (350, 270), 16, 1)
circle(screen, (255, 0, 0), (350, 270), 15, 7)
circle(screen, (0, 0, 0), (350, 270), 8, 8)
rect(screen, (0, 0, 0), (230, 370 , 140, 25))
polygon(screen, (0, 0, 0), [(170,200), (177,190), (297, 253), (290, 263)])
polygon(screen, (0, 0, 0), [(318,265), (314,255), (422, 213), (426, 223)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()