# following youtube tutorial, 'https://www.youtube.com/watch?v=AY9MnQ4x3zk'
from sys import exit
import pygame

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = score_font.render(str(current_time), False, (64, 64, 64)).convert()
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

# initialise variables
player_gravity = 0
player_isOnGround = False
game_active = True
start_time = 0

# initialise font
score_font = pygame.font.Font(('font/Pixeltype.ttf'), 50)

# initialise surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()

# initialise rectangles
snail_rect = snail_surface.get_rect(midbottom = (800, 300))
player_rect = player_surface.get_rect(midbottom = (80, 300))

while True:
    # calls all events in the game and runs through it one by one
    for event in pygame.event.get():
        # allows user to exit via default red button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # player is alive
        if game_active:
            # check for mouse click on player
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (player_rect.collidepoint(event.pos)):
                    if player_isOnGround:
                        player_gravity = -20

            # check for player jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_isOnGround:
                        player_gravity = -20
        
        # player is dead
        else:
            # restart game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    snail_rect.x = 800
                    game_active = True
                    start_time = pygame.time.get_ticks()
    
    # player is alive
    if game_active:
        # display surfaces
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        display_score()

        # snail movement
        if (snail_rect.x < -100): 
            snail_rect.x = 800
        else: 
            snail_rect.left -= 4
        screen.blit(snail_surface, snail_rect)

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        player_isOnGround = False
        if player_rect.bottom >= 300: 
            player_rect.bottom = 300
            player_isOnGround = True
        screen.blit(player_surface, player_rect)

        # collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    
    # player is dead
    else:
        screen.fill('Black')
        

    # update frames
    pygame.display.update()
    # frame rate ceiling of 60fps
    clock.tick(60)