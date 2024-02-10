import pygame

pygame.init()
font = pygame.font.Font(None, 30)

# function to display out info variable at x and y
def debug(info, x = 10, y = 10):
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x, y))
    pygame.draw.rect(display_surf, 'black', debug_rect)
    display_surf.blit(debug_surf, debug_rect)