import pygame
from player import Player

GAME_LOOP = True
WIDTH = 640
HEIGHT = 640
RESOLUTION = (WIDTH, HEIGHT)
TITLE_CAPTION = "Icy Tower"
FPS = 60

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(TITLE_CAPTION)

clock = pygame.time.Clock()

player = Player()


def exit_game(pressed_key):
    if pressed_key[pygame.K_ESCAPE]:
        return False
    return all(event.type != pygame.QUIT for event in pygame.event.get())


while GAME_LOOP:
    screen.fill(0)

    key_pressed = pygame.key.get_pressed()

    if not exit_game(key_pressed):
        GAME_LOOP = False

    player.move_player(key_pressed)

    screen.blit(player.current_frame, player.get_position())
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
quit()
