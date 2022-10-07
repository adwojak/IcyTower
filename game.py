import pygame
from player import Player
from wall import Background
from constants import GAME_WIDTH, GAME_HEIGHT, BACKGROUND_PNG

GAME_LOOP = True

RESOLUTION = (GAME_WIDTH, GAME_HEIGHT)
TITLE_CAPTION = "Icy Tower"
FPS = 30

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(TITLE_CAPTION)

clock = pygame.time.Clock()

player = Player()
background_group = Background()


def exit_game(pressed_key):
    if pressed_key[pygame.K_ESCAPE]:
        return False
    return all(event.type != pygame.QUIT for event in pygame.event.get())


while GAME_LOOP:
    screen.blit(pygame.image.load(BACKGROUND_PNG), (0, 0))

    key_pressed = pygame.key.get_pressed()

    if not exit_game(key_pressed):
        GAME_LOOP = False

    player.update(key_pressed, background_group)
    background_group.draw(screen)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
quit()
