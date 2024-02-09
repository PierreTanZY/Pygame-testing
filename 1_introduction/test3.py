from sys import exit
import pygame
from random import randint, choice

class Player(pygame.sprite.Sprite):
    # create player sprite
    def __init__(self):
        super().__init__()
        # import assests
        playerWalk1_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        playerWalk2_surface = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.playerWalk_surface = [playerWalk1_surface, playerWalk2_surface]
        self.playerWalk_index = 0
        self.playerJump_surface = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.playerWalk_surface[self.playerWalk_index]
        self.rect = self.image.get_rect(midbottom = (100, 300))
        self.gravity = 0

    # player jump
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            if soundToggle:
                jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.playerJump_surface
        else:
            self.playerWalk_index += 0.1
            if self.playerWalk_index >= len(self.playerWalk_surface):
                self.playerWalk_index = 0
            self.image = self.playerWalk_surface[int(self.playerWalk_index)]
    
    def reset(self):
        self.rect.midbottom = (80, 300)
        self.gravity = 0

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        # type is based on which obstacle it is
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 150

        elif type == 'snail':
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        else:
            debug.log("error, no obstacle sprites found")
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def movement(self):
        self.rect.x -= 6

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    def update(self):
        self.animation()
        self.movement()
        self.destroy()

class MusicButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        musicButton1_surface = pygame.image.load('graphics/buttons/music_button_1.png').convert_alpha()
        musicButton2_surface = pygame.image.load('graphics/buttons/music_button_2.png').convert_alpha()
        musicButton1_surface = pygame.transform.scale_by(musicButton1_surface, 3)
        musicButton2_surface = pygame.transform.scale_by(musicButton2_surface, 3)
        self.musicButton_surface = [musicButton1_surface, musicButton2_surface]
        self.musicButton_index = 0

        self.image = self.musicButton_surface[self.musicButton_index]
        self.rect = self.image.get_rect(center = (750, 50))
    
    def click(self):
        global musicToggle
        if musicToggle:
            background_music.stop()
            musicToggle = False
        else:
            background_music.play()
            musicToggle = True
    
    def animation(self):
        self.musicButton_index += 1
        if self.musicButton_index >= len(self.musicButton_surface):
            self.musicButton_index = 0
        self.image = self.musicButton_surface[self.musicButton_index]
    
    def update(self):
        self.click()
        self.animation()

class SoundButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        soundButton1_surface = pygame.image.load('graphics/buttons/sound_button_1.png').convert_alpha()
        soundButton2_surface = pygame.image.load('graphics/buttons/sound_button_2.png').convert_alpha()
        soundButton1_surface = pygame.transform.scale_by(soundButton1_surface, 3)
        soundButton2_surface = pygame.transform.scale_by(soundButton2_surface, 3)
        self.soundButton_surface = [soundButton1_surface, soundButton2_surface]
        self.soundButton_index = 0

        self.image = self.soundButton_surface[self.soundButton_index]
        self.rect = self.image.get_rect(center = (690, 50))

    def animation(self):
        self.soundButton_index += 1
        if self.soundButton_index >= len(self.soundButton_surface):
            self.soundButton_index = 0
        self.image = self.soundButton_surface[self.soundButton_index]

    def click(self):
        global soundToggle
        if soundToggle:
            soundToggle = False
        else:
            soundToggle = True
    
    def update(self):
        self.click()
        self.animation()

def collisions():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        return True
    else:
        return False

def end_game():
    global game_active
    game_active = False
    obstacle_group.empty()

def restart_game():
    global game_active
    global start_time
    game_active = True
    start_time = pygame.time.get_ticks()
    background_music.set_volume(musicVolume)
    Player.reset(player.sprite)

# regular pygame code
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

# initialise variables
game_active = True
start_time = 0
currentScore = 0
highScore = 0
soundToggle = True
soundVolume = 0.25
musicToggle = True
musicVolume = 0.1
musicVolume_menu = 0.03

# initialise/add sprite classes
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
musicButton = pygame.sprite.GroupSingle()
musicButton.add(MusicButton())
soundButton = pygame.sprite.GroupSingle()
soundButton.add(SoundButton())

# initialise font
pixel_font = pygame.font.Font(('font/Pixeltype.ttf'), 50)

# import sounds
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(soundVolume)
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(musicVolume)

# import surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
playerEndFrame_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
playerEndFrame_surface = pygame.transform.scale_by(playerEndFrame_surface, 2)
gameName_surface = pixel_font.render('Pixel Runner', False, (111, 196, 169)).convert()
gameName_surface = pygame.transform.scale_by(gameName_surface, 2)
gameMessage_surface = pixel_font.render('Press [spacebar] to run', False, (111, 196, 169))

# initialise rectangles
playerEndFrame_rect = playerEndFrame_surface.get_rect(center = (400,200))
gameName_rect = gameName_surface.get_rect(center = (400, 80))
gameMessage_rect = gameMessage_surface.get_rect(center = (400, 350))

# timer
obstacleSpawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleSpawn_timer, 1400)

# play background music
background_music.play(loops = -1)

while True:
    # calls all events in the game and runs through it one by one
    for event in pygame.event.get():
        # quit game via red button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # stop game via escape key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                end_game()

        # player is alive
        if game_active:
            # spawn obstacles
            if event.type == obstacleSpawn_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))

        # player is dead
        else:
            # restart game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart_game()

            # toggle music button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if musicButton.sprite.rect.collidepoint(pygame.mouse.get_pos()):
                    musicButton.update()

            # toggle sound button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if soundButton.sprite.rect.collidepoint(pygame.mouse.get_pos()):
                    soundButton.update()
    
    # player is alive
    if game_active:
        # display background surfaces
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        # update sprite classes
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        # check for end game conditions AKA collisions
        if collisions():
            end_game()

        # calculate current score
        currentScore = int((pygame.time.get_ticks() - start_time) / 1000)

        # display current score
        score_surface = pixel_font.render(f'Score: {currentScore}', False, (64, 64, 64)).convert()
        score_rect = score_surface.get_rect(center = (400, 50))
        screen.blit(score_surface, score_rect)

        # calculate highscore
        if currentScore > highScore:
            highScore = currentScore

    # player is dead
    else:
        # soften music volume
        background_music.set_volume(musicVolume_menu)

        # display game over screen
        screen.fill((94, 129, 162))
        screen.blit(playerEndFrame_surface, playerEndFrame_rect)
        screen.blit(gameName_surface, gameName_rect)
        screen.blit(gameMessage_surface, gameMessage_rect)

        # display score and highscore
        currentScore_surface = pixel_font.render(f'Your score: {currentScore}', False, (111,196,169))
        currentScore_rect = currentScore_surface.get_rect(center = (150, 200))
        screen.blit(currentScore_surface, currentScore_rect)
        highScore_surface = pixel_font.render(f'High score: {highScore}', False, (111, 196, 169))
        highScore_rect = highScore_surface.get_rect(center = (650, 200))
        screen.blit(highScore_surface, highScore_rect)

        # update sprite classes (buttons)
        musicButton.draw(screen)
        soundButton.draw(screen)
    
    # update frames
    pygame.display.update()
    # frame rate ceiling of 60fps
    clock.tick(60) 