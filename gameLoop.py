import pygame
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True
from player import player
from camera import camera
from map import twinleaf_town

while running:
    screen.fill((0 ,0, 0))
    camera.update_offset()
    camera.get_movement()
    camera.zoom_in()
    camera.draw_map(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.handle_event(event)
    player.set_movement()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
