import pygame, sys, time
from debug import debug

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

class Test(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # animation
        self.frames = [pygame.image.load(f'Rebi3/Rebi{i}.png').convert_alpha() for i in range(1,7)]
        self.frame_index = 0

        # image and rect
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midleft = (0,360))

        # variables
        self.rotation = 0
        self.direction = 1
        self.move_speed = 250
        self.animation_speed = 5
        self.pos = pygame.math.Vector2(self.rect.topleft)
    
    def animate(self):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def move(self):
        self.pos.x += self.direction * self.move_speed * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right > 1280 or self.rect.left < 0:
            self.direction *= -1

    def rotate(self):
        self.rotation += 100 * dt
        self.image = pygame.transform.rotozoom(self.image, self.rotation, 1)

    def update(self):
        self.animate()
        self.move()
        self.rotate()

test_group = pygame.sprite.Group()
test_group.add(Test())

prev_time = time.time()
while True:
    dt = time.time() - prev_time
    prev_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('white')

    test_group.update()
    test_group.draw(screen)
    debug(dt)

    pygame.display.update()
    clock.tick(60)