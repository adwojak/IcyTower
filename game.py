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

from constants import BACKGROUND_PNG, FPS, RESOLUTION, TITLE_CAPTION
from player import Player
from wall import generate_walls


def exit_game(pressed_key):
    if pressed_key[K_ESCAPE]:
        return False
    return all(event.type != QUIT for event in get_event())


def main():
    initialize_game()
    screen = set_mode(RESOLUTION)
    set_caption(TITLE_CAPTION)

    clock = Clock()

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
    main()
    quit_game()
    quit()
