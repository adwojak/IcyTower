from json import load as json_load

from pygame import Surface
from pygame.image import load as load_image

from constants import COLOR_BLACK


class SpriteSheetLoader:
    def __init__(self, sprite_sheet, definition):
        self.sprite_sheet = load_image(sprite_sheet)
        with open(definition) as file_stream:
            self.sprite_data = json_load(file_stream)

    def parse_sprites(self, names):
        return tuple(self.parse_sprite(name) for name in names)

    def parse_sprite(self, name):
        sprite_data = self.sprite_data["demon"][name]
        return self.get_sprite(
            sprite_data["x_position"], sprite_data["y_position"], sprite_data["width"], sprite_data["height"]
        )

    def get_sprite(self, x_position, y_position, width, height):
        surface = Surface((width, height))
        surface.set_colorkey(COLOR_BLACK)
        surface.blit(self.sprite_sheet, (0, 0), (x_position, y_position, width, height))
        return surface
