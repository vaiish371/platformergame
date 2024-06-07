import arcade
# from functions.load_texture_pair import load_texture_pair
import arcade


def load_texture_pair(filename):
    # load a texture of the asset and one that is flipped
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


RIGHT_FACING = 0
LEFT_FACING = 1


class PlayerCharacter(arcade.Sprite):
    def __init__(self, direction, scaling, updates_per_frame):
        super().__init__()

        # face right by default
        self.character_face_direction = direction
        self.cur_run_texture = 0
        self.cur_idle_texture = 0
        self.cur_hit_texture = 0
        self.scale = scaling
        self.updates_per_frame = updates_per_frame

        # track whether the player has landed
        self.landed = True

        # player health
        self.health = 3
        self.immune = False
        self.immune_wait = 0

        # player equipment
        self.weapon_list = list()

        # main path of assets
        run_path = "assets/Virtual Guy/run_sep/"
        idle_path = "assets/Virtual Guy/idle_sep/"
        jump_path = "assets/Virtual Guy/Jump (32x32).png"
        fall_path = "assets/Virtual Guy/Fall (32x32).png"
        hit_path = "assets/Virtual Guy/hit_sep/"

        # textures for jumping and falling
        self.jump_texture = load_texture_pair(jump_path)
        self.fall_texture = load_texture_pair(fall_path)

        # textures for idle animation
        self.idle_textures = []
        for i in range(11):
            texture = load_texture_pair(f"{idle_path}tile0{i}.png")
            self.idle_textures.append(texture)

        # textures for walk animation
        self.walk_textures = []
        for i in range(12):
            texture = load_texture_pair(f"{run_path}tile0{i}.png")
            self.walk_textures.append(texture)

        self.hit_textures = []
        for i in range(7):
            texture = load_texture_pair(f"{hit_path}tile0{i}.png")
            self.hit_textures.append(texture)

    # Updates the number of lives
    # If 0 lives, it will set game_over to True
    # Updates the scene
    def take_damage(self, scene_info, heart_list):
        if self.immune is False:
            self.health-=1
            heart_list.pop()

            if self.health == 0:
                scene_info.game_over = True
            else:
                scene_info.game_over = False
                self.immune = True

        return scene_info



    def update_animation(self, delta_time: float = 1 / 60):

        # change direction facing
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        self.cur_run_texture += 1
        self.cur_idle_texture += 1

        if self.cur_run_texture > 11 * self.updates_per_frame:
            self.cur_run_texture = 0
        if self.cur_idle_texture > 10 * self.updates_per_frame:
            self.cur_idle_texture = 0

        run_frame = self.cur_run_texture // self.updates_per_frame
        idle_frame = self.cur_idle_texture // self.updates_per_frame
        direction = self.character_face_direction

        # check if the player has been hit and is immune so the damage can't stack
        if self.immune is True:
            self.immune_wait += 1
            if self.immune_wait > 12 * self.updates_per_frame:
                self.immune_wait = 0
                self.immune = False

        # hit
        if self.immune is True:
            hit_frame = (self.immune_wait // 2) // self.updates_per_frame
            self.texture = self.hit_textures[hit_frame][direction]
            return

        # jumping
        if self.change_y > 0:
            self.texture = self.jump_texture[direction]
            return

        # falling
        elif self.change_y < 0:
            self.texture = self.fall_texture[direction]
            return

        # idle
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[idle_frame][direction]
            return

        # walking animation (not doing any of the other returns)
        self.texture = self.walk_textures[run_frame][direction]

