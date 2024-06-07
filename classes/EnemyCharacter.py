import arcade
#from functions.load_texture_pair import load_texture_pair
import arcade


def load_texture_pair(filename):
    # load a texture of the asset and one that is flipped
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

RIGHT_FACING = 0
LEFT_FACING = 1

class EnemyCharacter(arcade.Sprite):
    def __init__(self, name, scaling, updates_per_frame, e_run_path, e_hit_path, health, scale_mod=1.0, state="running", e_idle_path=None):
        super().__init__()

        # face right by default
        self.name = name
        self.enemy_face_direction = RIGHT_FACING
        self.cur_run_texture = 0
        self.cur_idle_texture = 0
        self.shoot_frame = 0
        self.scale = scaling*scale_mod
        self.updates_per_frame = updates_per_frame

        # shooting enemies
        self.bullet_delay = 1.5
        self.bullet_last = 0

        # state of running or idle
        self.state = state

        # need to define the hit box of the enemies
        # not sure why i don't need to for the player..?
        self.width = 20
        self.height = 26

        # define the health
        self.health = health
        self.immune = False
        self.immune_wait = 0

        if e_run_path is not None:
            # textures for walk animation
            self.walk_textures = []
            for i in range(12):
                texture = load_texture_pair(f"{e_run_path}tile0{i}.png")
                self.walk_textures.append(texture)

        if e_idle_path is not None:
            # textures for idle animation
            self.idle_textures = []
            for i in range(7):
                texture = load_texture_pair(f"{e_idle_path}tile0{i}.png")
                self.idle_textures.append(texture)

        # textures for hit animation
        self.hit_textures = []
        for i in range(4):
            texture = load_texture_pair(f"{e_hit_path}tile0{i}.png")
            self.hit_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # change direction facing
        if self.change_x > 0 and self.enemy_face_direction == RIGHT_FACING:
            self.enemy_face_direction = LEFT_FACING
        elif self.change_x < 0 and self.enemy_face_direction == LEFT_FACING:
            self.enemy_face_direction = RIGHT_FACING

        self.cur_run_texture += 1
        if self.cur_run_texture > 11 * self.updates_per_frame:
            self.cur_run_texture = 0

        self.cur_idle_texture += 1
        if self.cur_idle_texture > 24 * self.updates_per_frame:
            self.cur_idle_texture = 0

        idle_frame = (self.cur_idle_texture//4) // self.updates_per_frame
        self.shoot_frame = idle_frame
        run_frame = self.cur_run_texture // self.updates_per_frame
        direction = self.enemy_face_direction

        # check if the enemy has been hit and is immune so the damage can't stack
        if self.immune is True:
            self.immune_wait += 1
            if self.immune_wait > 6 * self.updates_per_frame:
                self.immune_wait = 0
                self.immune = False

        # getting hit
        if self.immune is True:
            hit_frame = (self.immune_wait//2) // self.updates_per_frame
            self.texture = self.hit_textures[hit_frame][direction]

            return

        if self.change_x != 0:
            # walking animation
            self.texture = self.walk_textures[run_frame][direction]
        else:
            self.texture = self.idle_textures[idle_frame][direction]
