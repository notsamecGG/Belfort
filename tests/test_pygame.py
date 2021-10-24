import sys, pygame
from pygame.constants import RESIZABLE

# init lib
pygame.init()

# Create window icon
icon = pygame.Surface((10, 10))
icon.fill((255, 255, 255))

# window settings
pygame.display.set_icon(icon)
pygame.display.set_caption("Name")
window = pygame.display.set_mode((800, 600), RESIZABLE)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
            pygame.quit()

    pygame.display.flip()