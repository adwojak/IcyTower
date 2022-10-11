from platform import generate_new_platforms, generate_starting_platforms

from pygame import K_ESCAPE, KEYUP, QUIT
from pygame import init as initialize_game
from pygame import quit as quit_game
from pygame.display import flip, set_caption, set_mode
from pygame.event import get as get_event
from pygame.image import load as load_image
from pygame.key import get_pressed
from pygame.sprite import Group
from pygame.time import Clock
from pygame_menu import Menu
from pygame_menu.themes import THEME_DARK

from constants import BACKGROUND_PNG, FPS, GAME_HEIGHT, GAME_WIDTH, RESOLUTION, TITLE_CAPTION
from player import Player
from wall import generate_walls


def exit_game(pressed_key):
    if pressed_key[K_ESCAPE]:
        return False
    return all(event.type != QUIT for event in get_event())


def perform_quit():
    quit_game()
    quit()


def main(screen, clock):
    player_group = Group()
    walls_group = Group(generate_walls())
    platforms_group = Group(generate_starting_platforms())

    player = Player()
    player_group.add(player)

    background_image = load_image(BACKGROUND_PNG)

    while player.is_alive:
        screen.blit(background_image, (0, 0))

        key_pressed = get_pressed()
        key_up_events = [key.key for key in get_event(KEYUP)]

        if not exit_game(key_pressed):
            return

        generate_new_platforms(platforms_group)
        player.move(key_pressed, key_up_events, [walls_group, platforms_group])

        player_group.update()
        platforms_group.update()

        platforms_group.draw(screen)
        walls_group.draw(screen)
        player_group.draw(screen)

        flip()
        clock.tick(FPS)


if __name__ == "__main__":
    initialize_game()
    _screen = set_mode(RESOLUTION)
    set_caption(TITLE_CAPTION)
    _clock = Clock()

    menu = Menu(TITLE_CAPTION, GAME_WIDTH, GAME_HEIGHT, theme=THEME_DARK)
    menu.add.button("Start", main, _screen, _clock)
    menu.add.button("Exit", perform_quit)
    menu.mainloop(_screen)

    perform_quit()
