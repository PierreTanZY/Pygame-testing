from sys import exit
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

while True:
    # calls all events in the game and runs through it one by one
    for event in pygame.event.get():
        # allows user to exit via default red button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()

    # frame rate ceiling of 60fps
    clock.tick(60)