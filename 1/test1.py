from sys import exit
import pygame
from random import randint

# function to calculate/show score
def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surface = pixel_font.render(f'Score: {current_time}', False, (64, 64, 64)).convert()
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

# function to move obstacles
def obstacle_movement(obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle_rect in obstacle_rect_list:
            if obstacle_rect.x < -100:
                obstacle_rect_list.remove(obstacle_rect)
            else:
                obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            elif obstacle_rect.bottom == 150:
                screen.blit(fly_surface, obstacle_rect)
        return obstacle_rect_list
    else:
        return[]

# collision between player and obstacle
def collisions(player, obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect):
                backgroundMusic_sound.fadeout(1000)
                return False
        return True
    else:
        return True

# player animation
def player_animation():
    global player_surface, playerWalk_index
    # jump animation
    if player_rect.bottom < 300:
        player_surface = playerJump_surface
    # walk animation
    else:
        playerWalk_index += 0.1
        if playerWalk_index >= len(playerWalk_surface):
            playerWalk_index = 0
        player_surface = playerWalk_surface[int(playerWalk_index)]

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

# initialise variables
player_gravity = 0
player_isOnGround = False
game_active = True
start_time = 0
highScore = 0
currentScore = 0
obstacle_rect_list = []

# initialise font
pixel_font = pygame.font.Font(('font/Pixeltype.ttf'), 50)

# import sounds
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.5)
backgroundMusic_sound = pygame.mixer.Sound('audio/music.wav')
backgroundMusic_sound.set_volume(0.25)
backgroundMusic_sound.play(loops = -1)

# import surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
snailFrame1_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snailFrame2_surface = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snailFrame_surface = [snailFrame1_surface, snailFrame2_surface]
snailFrame_index = 0
snail_surface = snailFrame_surface[snailFrame_index]

flyFrame1_surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
flyFrame2_surface = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
flyFrame_surface = [flyFrame1_surface, flyFrame2_surface]
flyFrame_index = 0
fly_surface = flyFrame_surface[flyFrame_index]

playerWalk1_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
playerWalk2_surface = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
playerWalk_surface = [playerWalk1_surface, playerWalk2_surface]
playerWalk_index = 0
playerJump_surface = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_surface = playerWalk_surface[playerWalk_index]

playerStand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
playerStand_surface = pygame.transform.scale_by(playerStand_surface, 2)
gameName_surface = pixel_font.render('Pixel Runner', False, (111, 196, 169)).convert()
gameName_surface = pygame.transform.scale_by(gameName_surface, 2)
gameMessage_surface = pixel_font.render('Press [spacebar] to run', False, (111, 196, 169))

# initialise rectangles
player_rect = player_surface.get_rect(midbottom = (80, 300))
playerStand_rect = playerStand_surface.get_rect(center = (400,200))
gameName_rect = gameName_surface.get_rect(center = (400, 80))
gameMessage_rect = gameMessage_surface.get_rect(center = (400, 350))

# Timer
obstacleSpawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleSpawn_timer, 1400)

snailAnimation_timer  = pygame.USEREVENT + 2
pygame.time.set_timer(snailAnimation_timer, 500)

flyAnimation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(flyAnimation_timer, 200)

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
                        jump_sound.play()

            # spawn, move and delete obstacles
            if event.type == obstacleSpawn_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900,1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900,1100), 150)))
            
            if event.type == snailAnimation_timer:
                snailFrame_index += 1
                if snailFrame_index >= len(snailFrame_surface):
                    snailFrame_index = 0
                snail_surface = snailFrame_surface[int(snailFrame_index)]
            
            if event.type == flyAnimation_timer:
                flyFrame_index += 1
                if flyFrame_index >= len(flyFrame_surface):
                    flyFrame_index = 0
                fly_surface = flyFrame_surface[int(flyFrame_index)]

        # player is dead
        else:
            # restart game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()
                    backgroundMusic_sound.play(loops = -1)
    
    # player is alive
    if game_active:
        # display surfaces
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        currentScore = display_score()
        if currentScore > highScore:
            highScore = currentScore

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        player_isOnGround = False
        if player_rect.bottom >= 300: 
            player_rect.bottom = 300
            player_isOnGround = True
        player_animation()
        screen.blit(player_surface, player_rect)

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collisions(player_rect, obstacle_rect_list)
    
    # player is dead
    else:
        # reset obstacles and player
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        # display game over screen
        screen.fill((94, 129, 162))
        screen.blit(playerStand_surface, playerStand_rect)
        screen.blit(gameName_surface, gameName_rect)
        screen.blit(gameMessage_surface, gameMessage_rect)

        # display score and highscore
        currentScore_surface = pixel_font.render(f'Your score: {currentScore}', False, (111,196,169))
        currentScore_rect = currentScore_surface.get_rect(center = (150, 200))
        screen.blit(currentScore_surface, currentScore_rect)
        highScore_surface = pixel_font.render(f'High score: {highScore}', False, (111, 196, 169))
        highScore_rect = highScore_surface.get_rect(center = (650, 200))
        screen.blit(highScore_surface, highScore_rect)
    
        
    # update frames
    pygame.display.update()
    # frame rate ceiling of 60fps
    clock.tick(60)