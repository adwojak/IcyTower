import pygame

from constants import GRAVITY_VALUE, GAME_HEIGHT, VERTICAL_ACCELERATION_STARTING_VALUE, VERTICAL_ACCELERATION_CHANGE_VALUE, HORIZONTAL_ACCELERATION_VALUE, HORIZONTAL_ACCELERATION_MIN, HORIZONTAL_ACCELERATION_MAX, HORIZONTAL_ACCELERATION_UPPER_LIMIT, HORIZONTAL_ACCELERATION_LOWER_LIMIT
from sprite_sheet_loader import SpriteSheetLoader

STATE_IDLE = "idle"
STATE_MOVE_LEFT = "move_left"
STATE_MOVE_RIGHT = "move_right"
STATE_JUMP = "jump"


class Player(pygame.sprite.Sprite):
    WALKING_FRAMES_NAMES = ("walk_0", "walk_1", "walk_0", "walk_2")
    IDLE_FRAMES_NAMES = ("idle_0", "idle_1", "idle_2", "idle_3")
    JUMP_NAME = "rotate"

    x = 300.0
    y = 550.0
    state = STATE_IDLE
    last_updated = 0
    current_frame_index = 0
    horizontal_acceleration = 0.0
    vertical_acceleration = 0.0
    currently_jumping = False
    jump_blocked = False
    on_platform = False
    is_alive = True

    current_frame = None
    idle_frames = None
    rotate_frame = None
    jump_frame = None
    walking_frames_right = None
    walking_frames_left = None

    states_map = {}

    def __init__(self):
        super().__init__()
        self.load_frames()

    def get_position(self):
        return self.x, self.y

    def get_rect(self):
        rect = self.current_frame.get_rect()
        rect.x, rect.y = self.x, self.y
        return rect

    def draw(self, base_surface):
        if self.y > GAME_HEIGHT:
            self.is_alive = False
            self.kill()
        base_surface.blit(self.current_frame, self.get_position())

    def update(self, key_pressed, keys_up, collision_groups):
        self.move_player(key_pressed, keys_up)
        for group in collision_groups:
            self.check_collisions(group)
        self.set_state()
        self.animate()

    def update_vertical(self, value):
        self.y += value
        self.rect.y += value

    def update_horizontal(self, value):
        self.x += value
        self.rect.x += value

    def move_player(self, key_pressed, keys_up):
        self.calculate_move(key_pressed, keys_up)
        self.include_gravity()

    def calculate_move(self, key_pressed, keys_up):
        if key_pressed[pygame.K_LEFT]:
            self.accelerate_left()
        elif key_pressed[pygame.K_RIGHT]:
            self.accelerate_right()
        else:
            self.decrease_acceleration()

        if pygame.K_SPACE in keys_up:
            if not self.jump_blocked:
                self.proceed_jump()
        else:
            self.decrease_vertical_acceleration()

        self.update_horizontal(self.horizontal_acceleration)
        self.update_vertical(-self.vertical_acceleration)

    def include_gravity(self):
        self.update_vertical(1 if self.on_platform else GRAVITY_VALUE)

    def proceed_jump(self):
        self.currently_jumping = True
        self.vertical_acceleration = VERTICAL_ACCELERATION_STARTING_VALUE - 1

    def check_collisions(self, background_group):
        collisions_sprites = pygame.sprite.spritecollide(self, background_group, False)
        self.on_platform = False
        self.jump_blocked = True
        for sprite in collisions_sprites:
            if sprite.collision_side == "top":
                self.on_platform = True
                if not self.currently_jumping:
                    self.y = sprite.rect.top + 5.0 - self.rect.height
                    self.jump_blocked = False
                    self.vertical_acceleration = 0.0
            elif sprite.collision_side == "right":
                self.x = sprite.rect.right
                self.horizontal_acceleration = 0.0
            elif sprite.collision_side == "left":
                self.x = sprite.rect.left - self.rect.width
                self.horizontal_acceleration = 0.0

    def set_state(self):
        if self.vertical_acceleration != 0.0:
            self.state = STATE_JUMP
        elif self.horizontal_acceleration < 0.0:
            self.state = STATE_MOVE_LEFT
        elif self.horizontal_acceleration > 0.0:
            self.state = STATE_MOVE_RIGHT
        else:
            self.state = STATE_IDLE

    def animate(self):
        current_ticks = pygame.time.get_ticks()
        if self.state == STATE_JUMP:
            self.last_updated = current_ticks
            self.current_frame_index = 0
            self.current_frame = self.jump_frame
        if self.state.startswith("move") and current_ticks - self.last_updated > 100:
            self.last_updated = current_ticks
            frames_tuple = self.states_map[self.state]
            self.current_frame_index = (self.current_frame_index + 1) % len(frames_tuple)
            self.current_frame = frames_tuple[self.current_frame_index]
        elif current_ticks - self.last_updated > 150:
            self.last_updated = current_ticks
            self.current_frame_index = (self.current_frame_index + 1) % len(self.idle_frames)
            self.current_frame = self.idle_frames[self.current_frame_index]
        self.rect = self.get_rect()

    def accelerate_right(self):
        self.horizontal_acceleration += HORIZONTAL_ACCELERATION_VALUE
        self.horizontal_acceleration = min(self.horizontal_acceleration, HORIZONTAL_ACCELERATION_UPPER_LIMIT)

    def accelerate_left(self):
        self.horizontal_acceleration -= HORIZONTAL_ACCELERATION_VALUE
        self.horizontal_acceleration = max(self.horizontal_acceleration, HORIZONTAL_ACCELERATION_LOWER_LIMIT)

    def decrease_acceleration(self):
        if HORIZONTAL_ACCELERATION_MIN < self.horizontal_acceleration < HORIZONTAL_ACCELERATION_MAX:
            self.horizontal_acceleration = 0.0
        elif self.horizontal_acceleration >= HORIZONTAL_ACCELERATION_MAX:
            self.horizontal_acceleration -= HORIZONTAL_ACCELERATION_VALUE
        else:
            self.horizontal_acceleration += HORIZONTAL_ACCELERATION_VALUE

    def decrease_vertical_acceleration(self):
        if self.jump_blocked:
            self.vertical_acceleration -= VERTICAL_ACCELERATION_CHANGE_VALUE
            if self.vertical_acceleration <= 0.0:
                self.currently_jumping = False

    def load_frames(self):
        sprite_sheet_loader = SpriteSheetLoader("sprites/demon_sheet.png", "sprites/definitions.json")
        self.idle_frames = sprite_sheet_loader.parse_sprites(self.IDLE_FRAMES_NAMES)
        self.jump_frame = sprite_sheet_loader.parse_sprite(self.JUMP_NAME)
        self.walking_frames_right = sprite_sheet_loader.parse_sprites(self.WALKING_FRAMES_NAMES)
        self.walking_frames_left = tuple(
            pygame.transform.flip(frame, True, False) for frame in self.walking_frames_right
        )
        self.current_frame = self.idle_frames[0]
        self.rect = self.get_rect()

        self.states_map = {
            STATE_MOVE_LEFT: self.walking_frames_left,
            STATE_MOVE_RIGHT: self.walking_frames_right,
        }
