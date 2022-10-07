import pygame

from constants import PLATFORM_ELEMENT_HEIGHT, PLATFORM_ELEMENT_WIDTH, PLATFORM_MIDDLE, PLATFORM_START

LEFT_SIDE_IMAGE = pygame.image.load(PLATFORM_START)
MIDDLE_IMAGE = pygame.image.load(PLATFORM_MIDDLE)
RIGHT_SIDE_IMAGE = pygame.transform.flip(LEFT_SIDE_IMAGE, True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(
        self, x_position, y_position, collision_side, middle_repeats, left_side_image, middle_image, right_side_image
    ):
        super().__init__()
        self.x = x_position
        self.y = y_position
        self.collision_side = collision_side
        self.left_side_image = left_side_image
        self.middle_image = middle_image
        self.right_side_image = right_side_image
        self.surface = self.generate_platform(middle_repeats)
        self.rect = self.get_rect()
        pygame.draw.rect(self.surface, (255, 0, 0), self.surface.get_rect(), 1)

    def generate_platform(self, middle_repeats):
        width = PLATFORM_ELEMENT_WIDTH * (middle_repeats + 2)
        surface = pygame.Surface((width, PLATFORM_ELEMENT_HEIGHT))
        surface.blit(self.left_side_image, (0, 0))
        for element in range(middle_repeats):
            surface.blit(self.middle_image, ((element + 1) * PLATFORM_ELEMENT_WIDTH, 0))
        surface.blit(self.right_side_image, (width - PLATFORM_ELEMENT_WIDTH, 0))
        return surface

    def get_rect(self):
        rect = self.surface.get_rect()
        rect.x = self.x
        rect.y = self.y
        return rect

    def get_position(self):
        return self.x, self.y

    def draw(self, base_surface):
        base_surface.blit(self.surface, self.get_position())


class PlatformGenerator:
    @staticmethod
    def generate_single_platform(x_position, y_position, middle_repeats):
        return Platform(x_position, y_position, "top", middle_repeats, LEFT_SIDE_IMAGE, MIDDLE_IMAGE, RIGHT_SIDE_IMAGE)
