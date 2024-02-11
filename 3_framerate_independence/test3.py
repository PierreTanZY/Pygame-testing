import pygame, sys, time
from debug import debug

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

test_rect = pygame.Rect(0, 310, 100, 100)
test_rect_pos = test_rect.x
test_speed = 200

previous_time = time.time()
while True:
    dt = time.time() - previous_time
    previous_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('white')

    # rect movement and drawing
    test_rect_pos += test_speed * dt
    test_rect.x = round(test_rect_pos)
    pygame.draw.rect(screen, 'red', test_rect)

    debug(dt)
    pygame.display.update()

# first method to have framerate independence, 
# use clock.tick to get dt amd multiply dt with any movement in the game.
# + simple to understand
# - must increase movement speed to compensate
# - not very precise