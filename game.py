import pygame
from player import Player
from wall import BackgroundGroup
from constants import GAME_WIDTH, GAME_HEIGHT, BACKGROUND_PNG
from platform import PlatformGroup

GAME_LOOP = True

RESOLUTION = (GAME_WIDTH, GAME_HEIGHT)
TITLE_CAPTION = "Icy Tower"
FPS = 30

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(TITLE_CAPTION)

clock = pygame.time.Clock()

player = Player()
background_group = BackgroundGroup()
platform_group = PlatformGroup()


def exit_game(pressed_key):
    if pressed_key[pygame.K_ESCAPE]:
        return False
    return all(event.type != pygame.QUIT for event in pygame.event.get())


while GAME_LOOP:
    screen.blit(pygame.image.load(BACKGROUND_PNG), (0, 0))

    key_pressed = pygame.key.get_pressed()
    key_up_events = [key.key for key in pygame.event.get(pygame.KEYUP)]

    if not exit_game(key_pressed):
        GAME_LOOP = False

    player.update(key_pressed, key_up_events, [background_group, platform_group])
    platform_group.draw(screen)
    background_group.draw(screen)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
quit()

# TODO
# Wejście na platformę z boku
# Zwiększanie prędkości
# Usunięcie tła z postaci
