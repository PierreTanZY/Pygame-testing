import pygame, sys
from debug import debug

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

test_rect = pygame.Rect(0, 310, 100, 100)
test_speed = 200

while True:
    dt = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('white')

    # rect movement and drawing
    test_rect.x += test_speed * dt
    pygame.draw.rect(screen, 'red', test_rect)

    debug(dt)
    pygame.display.update()

# first method to have framerate independence, 
# use clock.tick to get dt amd multiply dt with any movement in the game.
# + simple to understand
# - must increase movement speed to compensate
# - not very precise