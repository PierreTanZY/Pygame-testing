# following youtube tutorial, 'https://www.youtube.com/watch?v=AY9MnQ4x3zk'

from sys import exit
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

# initialise variables
player_gravity = 0

# initialise font
score_font = pygame.font.Font(('font/Pixeltype.ttf'), 50)

# initialise surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
score_surface = score_font.render('My game', False, (64, 64, 64)).convert()
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()

# initialise rectangles
score_rect = score_surface.get_rect(center = (400, 50))
snail_rect = snail_surface.get_rect(midbottom = (800, 300))
player_rect = player_surface.get_rect(midbottom = (80, 300))

while True:
    # calls all events in the game and runs through it one by one
    for event in pygame.event.get():
        # allows user to exit via default red button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # check for mouse click on player
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (player_rect.collidepoint(event.pos)):
                player_gravity = -20

        # check for player jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_gravity = -20
    
    # display surfaces
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    pygame.draw.rect(screen, '#c0e8ec', score_rect)
    screen.blit(score_surface, score_rect)

    # snail movement
    if (snail_rect.x < -100): 
        snail_rect.x = 800
    else: 
        snail_rect.left -= 4
    screen.blit(snail_surface, snail_rect)

    # player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 300: 
        player_rect.bottom = 300
    screen.blit(player_surface, player_rect)

    # update frames
    pygame.display.update()
    # frame rate ceiling of 60fps
    clock.tick(60)