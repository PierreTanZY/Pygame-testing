import pygame, sys
from debug import debug

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
rebi_surf = pygame.image.load('Rebi2.png').convert_alpha()
rebi_surf = pygame.transform.scale_by(rebi_surf, 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('white')
    screen.blit(rebi_surf, (75,50))

    # debug
    debug(pygame.mouse.get_pos())
    debug('test', 0, 40)
    debug('mouse!', pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    pygame.display.update()
    clock.tick(60)