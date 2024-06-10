import arcade

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 650

def load_texture_pair(filename):
    # load a texture of the asset and one that is flipped
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class Item(arcade.Sprite):
    def __init__(self, name, scaling, sprite_native, gui_scaling, updates_per_frame, i_path, c_path):
        super().__init__()

        self.name = name
        self.cur_float_texture = 0
        self.cur_collect_texture = 0
        self.scale = scaling
        self.updates_per_frame = updates_per_frame
        self.sprite_native = sprite_native
        self.gui_scaling = gui_scaling
        self.collected = False
        self.collect_wait = 0

        # textures for floating animation
        self.float_textures = []
        for i in range(16):
            texture = load_texture_pair(f"{i_path}tile0{i}.png")
            self.float_textures.append(texture)

        # textures for collection animation
        self.collect_textures = []
        for i in range(6):
            texture = load_texture_pair(f"{c_path}tile0{i}.png")
            self.collect_textures.append(texture)

    def run_behavior(self, player, heart_list):
        if self.name == "health":
            new_heart = arcade.Sprite("assets/heart_32x32.png")
            new_heart.top = SCREEN_HEIGHT - 20
            new_heart.left = heart_list[-1].left + self.sprite_native + 10  # buffer of 10 pixels
            heart_list.append(new_heart)
            player.health += 1
            return player, heart_list

        return player, heart_list

    def update_animation(self, delta_time: float = 1 / 60):

        self.cur_float_texture += 1
        if self.cur_float_texture > 15 * self.updates_per_frame:
            self.cur_float_texture = 0

        float_frame = self.cur_float_texture // self.updates_per_frame

        # check if the item is collected to play the collected animation
        if self.collected is True:
            self.collect_wait += 1
            if self.collect_wait > 5 * self.updates_per_frame:
                self.collect_wait = 0
                # mark_object for removal
                self.remove_from_sprite_lists()
                self.collected = False

        if self.collected is True:
            collect_frame = (self.collect_wait // 2) // self.updates_per_frame
            self.texture = self.collect_textures[collect_frame][0]

            return

        # floating animation
        self.texture = self.float_textures[float_frame][0]
