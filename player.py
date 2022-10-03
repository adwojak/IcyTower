import pygame

from sprite_sheet_loader import SpriteSheetLoader

STATE_IDLE = "idle"
STATE_MOVE_LEFT = "move_left"
STATE_MOVE_RIGHT = "move_right"
STATE_JUMP = "jump"
STATE_JUMP_LEFT = "jump_left"
STATE_JUMP_RIGHT = "jump_right"


class Player(pygame.sprite.Sprite):
    JUMP_HEIGHT = 5
    MAXIMUM_JUMP_HEIGHT = 20 * JUMP_HEIGHT

    HORIZONTAL_ACCELERATION_VALUE = 0.5
    HORIZONTAL_ACCELERATION_MIN = -3 * HORIZONTAL_ACCELERATION_VALUE
    HORIZONTAL_ACCELERATION_MAX = 3 * HORIZONTAL_ACCELERATION_VALUE
    HORIZONTAL_ACCELERATION_UPPER_LIMIT = 20 * HORIZONTAL_ACCELERATION_VALUE
    HORIZONTAL_ACCELERATION_LOWER_LIMIT = -1 * HORIZONTAL_ACCELERATION_UPPER_LIMIT

    WALKING_FRAMES_NAMES = ("walk_0", "walk_1", "walk_0", "walk_2")
    JUMPING_FRAMES_NAMES = ("jump_0", "jump_1", "jump_2", "jump_3")
    IDLE_FRAMES_NAMES = ("idle_0", "idle_1", "idle_2", "idle_3")
    EDGE_FRAMES_NAMES = ("edge_0", "edge_1")
    ROTATE_NAME = "rotate"

    state = STATE_IDLE
    last_updated = 0
    current_frame_index = 0
    horizontal_acceleration = 0.0
    x_current = 300
    y_current = 300

    current_frame = None
    idle_frames = None
    rotate_frame = None
    walking_frames_right = None
    walking_frames_left = None
    jumping_frames_right = None
    jumping_frames_left = None
    edge_frames_right = None
    edge_frames_left = None

    states_map = {}

    def __init__(self):
        super().__init__()
        self.load_frames()
        self.jump_available = True
        self.currently_jumping = False
        self.jump_height = 0  # TMP do wywalenia, potem sprawdzamy czy dotyka czegos

    def calculate_move(self, key_pressed):
        if key_pressed[pygame.K_LEFT]:
            self.accelerate_left()
        elif key_pressed[pygame.K_RIGHT]:
            self.accelerate_right()
        else:
            self.decrease_acceleration()

        if key_pressed[pygame.K_SPACE]:
            self.proceed_jump()

    def update(self, key_pressed):
        self.move_player(key_pressed)
        self.set_state()
        self.animate()

    def move_player(self, key_pressed):
        self.calculate_move(key_pressed)
        self.x_current += self.horizontal_acceleration
        self.jump()

    def set_state(self):
        if self.jump_height:
            if self.horizontal_acceleration < 0:
                self.state = STATE_JUMP_LEFT
            elif self.horizontal_acceleration > 0:
                self.state = STATE_JUMP_RIGHT
            else:
                self.state = STATE_JUMP
        elif self.horizontal_acceleration < 0:
            self.state = STATE_MOVE_LEFT
        elif self.horizontal_acceleration > 0:
            self.state = STATE_MOVE_RIGHT
        else:
            self.state = STATE_IDLE

    def animate(self):
        current_ticks = pygame.time.get_ticks()
        if (
            self.state.startswith("move") or self.state.startswith("jump_")
        ) and current_ticks - self.last_updated > 100:
            self.last_updated = current_ticks
            frames_tuple = self.states_map[self.state]
            self.current_frame_index = (self.current_frame_index + 1) % len(frames_tuple)
            self.current_frame = frames_tuple[self.current_frame_index]
        elif self.state == STATE_JUMP and current_ticks - self.last_updated > 100:
            self.last_updated = current_ticks
            self.current_frame_index = 0
            self.current_frame = self.jumping_frames_right[0]
        elif current_ticks - self.last_updated > 150:
            self.last_updated = current_ticks
            self.current_frame_index = (self.current_frame_index + 1) % len(self.idle_frames)
            self.current_frame = self.idle_frames[self.current_frame_index]

        pygame.draw.rect(self.current_frame, (255, 0, 0), self.current_frame.get_rect(), 1)

    def jump(self):
        if self.jump_available:
            return
        if self.currently_jumping:
            self.y_current -= self.JUMP_HEIGHT
            self.jump_height += self.JUMP_HEIGHT
            if self.jump_height > self.MAXIMUM_JUMP_HEIGHT:
                self.currently_jumping = False
        else:
            self.y_current += self.JUMP_HEIGHT
            self.jump_height -= self.JUMP_HEIGHT
            if self.jump_height <= 0:
                self.jump_available = True

    def proceed_jump(self):
        if self.jump_available:
            self.jump_available = False
            self.currently_jumping = True

    def accelerate_right(self):
        self.horizontal_acceleration += self.HORIZONTAL_ACCELERATION_VALUE
        self.horizontal_acceleration = min(self.horizontal_acceleration, self.HORIZONTAL_ACCELERATION_UPPER_LIMIT)

    def accelerate_left(self):
        self.horizontal_acceleration -= self.HORIZONTAL_ACCELERATION_VALUE
        self.horizontal_acceleration = max(self.horizontal_acceleration, self.HORIZONTAL_ACCELERATION_LOWER_LIMIT)

    def decrease_acceleration(self):
        if self.HORIZONTAL_ACCELERATION_MIN < self.horizontal_acceleration < self.HORIZONTAL_ACCELERATION_MAX:
            self.horizontal_acceleration = 0
        elif self.horizontal_acceleration >= self.HORIZONTAL_ACCELERATION_MAX:
            self.horizontal_acceleration -= self.HORIZONTAL_ACCELERATION_VALUE
        else:
            self.horizontal_acceleration += self.HORIZONTAL_ACCELERATION_VALUE

    def get_position(self):
        return self.x_current, self.y_current

    def load_frames(self):
        sprite_sheet_loader = SpriteSheetLoader("sprites/demon_sheet.png", "sprites/definitions.json")
        self.idle_frames = sprite_sheet_loader.parse_sprites(self.IDLE_FRAMES_NAMES)
        self.rotate_frame = sprite_sheet_loader.parse_sprite(self.ROTATE_NAME)
        self.walking_frames_right = sprite_sheet_loader.parse_sprites(self.WALKING_FRAMES_NAMES)
        self.walking_frames_left = tuple(
            pygame.transform.flip(frame, True, False) for frame in self.walking_frames_right
        )
        self.jumping_frames_right = sprite_sheet_loader.parse_sprites(self.JUMPING_FRAMES_NAMES)
        self.jumping_frames_left = tuple(
            pygame.transform.flip(frame, True, False) for frame in self.jumping_frames_right
        )
        self.edge_frames_right = sprite_sheet_loader.parse_sprites(self.EDGE_FRAMES_NAMES)
        self.edge_frames_left = tuple(pygame.transform.flip(frame, True, False) for frame in self.edge_frames_right)
        self.current_frame = self.idle_frames[0]

        self.states_map = {
            STATE_JUMP_LEFT: self.jumping_frames_left,
            STATE_JUMP_RIGHT: self.jumping_frames_right,
            STATE_MOVE_LEFT: self.walking_frames_left,
            STATE_MOVE_RIGHT: self.walking_frames_right,
        }
