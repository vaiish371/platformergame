import arcade
import arcade.gui

from classes.Item import Item
# from functions.load_texture_pair import load_texture_pair
from classes.PlayerCharacter import PlayerCharacter
from classes.EnemyCharacter import EnemyCharacter
from views.MenuView import MenuView
from views.PauseView import PauseView
from views.GameOverView import GameOverView

def load_texture_pair(filename):
    # load a texture of the asset and one that is flipped
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

SCREEN_WIDTH = 480 * 2
SCREEN_HEIGHT = 320 * 2
SCREEN_TITLE = "Thursday's Platformer Game!"

TILE_SIZE = 16
SPRITE_NATIVE_SIZE = 32

CHARACTER_SCALING = 2
ENEMY_SCALING = 2
ITEM_SCALING = 2
GUI_SCALING = 4

TILE_SCALING = 2
GRID_PIXEL_SIZE = TILE_SIZE * TILE_SCALING
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * CHARACTER_SCALING)

GRAVITY = 0.6

MOVEMENT_SPEED = 3 * CHARACTER_SCALING
PLAYER_JUMP_SPEED = 6 * CHARACTER_SCALING

ENEMY_SPEED = 2

UPDATES_PER_FRAME = 4

# fixed values for determining direction
RIGHT_FACING = 0
LEFT_FACING = 1

MUSIC_PATH = "assets/sounds/bg.wav"
MUSIC_VOLUME = 0.1

ITEM_SCALING = 2


class MyGame(arcade.View):
    def __init__(self, music_path):
        super().__init__()

        # ost
        self.music_path = music_path
        self.music = None
        self.currently_playing = None

        # tile map
        self.tile_map = None
        self.physics_engine = None
        self.scene = None
        self.end_of_map = 0
        self.going = True  # check if the player is going backwards to previous level

        # game over
        self.game_over = False

        # player attribute
        self.player = None

        # level number
        self.max_level = 3
        self.level = 3

        # cameras
        self.screen_center_x = 0
        self.screen_center_y = 0
        self.camera = None
        self.camera_gui = None

        self.heart_list = None
        self.weapon_gui_list = None

    def setup(self):
        self.player = PlayerCharacter(RIGHT_FACING, CHARACTER_SCALING, UPDATES_PER_FRAME)
        self.level = 1
        self.heart_list = arcade.SpriteList()
        self.weapon_gui_list = arcade.SpriteList()

        pos = 30
        for _ in range(self.player.health):
            heart = arcade.Sprite("assets/heart_32x32.png")
            heart.top = SCREEN_HEIGHT - 20
            heart.left = pos
            pos+=SPRITE_NATIVE_SIZE + 20
            self.heart_list.append(heart)

        if self.music is not None:
            # checks if the Music Player object has music is playing
            # re-loops the music after game is restarted
            if self.music.is_playing(self.currently_playing) is True:
                self.music.stop(self.currently_playing)
        self.music = arcade.Sound(self.music_path, streaming=True)
        self.currently_playing = self.music.play(MUSIC_VOLUME, loop=True)

        self.load_level(self.level)

    def load_level(self, level):
        # set the tile map as the current level here
        map_name = "tiled_maps/level{0}.tmx".format(level)

        # layer options
        layer_options = {
            "Terrain": {
                "use_spatial_hash": True,
            },
            "Traps": {
                "use_spatial_hash": False,
            },
            "Items": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING, layer_options=layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # add the player sprite
        self.scene.add_sprite("Player", self.player)

        # calculate the right edge of the map in pixels
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # set the player position based on whether he is
        # going forward or backward through levels
        if self.going is False:
            # im going backwards
            self.player.right = self.end_of_map
            self.player.center_y = 1 * GRID_PIXEL_SIZE
            self.player.character_face_direction = LEFT_FACING
        else:
            # im going forward so put me on the left side
            self.player.center_x = 1 * GRID_PIXEL_SIZE
            self.player.center_y = 1 * GRID_PIXEL_SIZE

        # load in the enemies of that level
        if "Enemies" in self.tile_map.object_lists:
            enemies_layer = self.tile_map.object_lists["Enemies"]
            for ene in enemies_layer:
                # cartesian converts the position into tile position
                cartesian = self.tile_map.get_cartesian(
                    abs(ene.shape[0]), abs(ene.shape[1])
                )
                enemy_type = ene.properties["name"]
                # assign the textures for the enemy in question
                if enemy_type == "chicken":
                    enemy = EnemyCharacter(
                        "chicken", ENEMY_SCALING, UPDATES_PER_FRAME,
                        "assets/Enemies/Chicken/run_sep/", "assets/Enemies/Chicken/hit_sep/", 100
                    )
                elif enemy_type == "bunny":
                    enemy = EnemyCharacter(
                        "bunny", ENEMY_SCALING, UPDATES_PER_FRAME,
                        "assets/Enemies/Bunny/run_sep/", "assets/Enemies/Bunny/hit_sep/", 150, scale_mod=0.773
                    )
                elif enemy_type == "plant":
                    enemy = EnemyCharacter(
                        "plant", ENEMY_SCALING, UPDATES_PER_FRAME,
                        None, "assets/Enemies/Plant/hit_sep/", 100,
                        e_idle_path="assets/Enemies/Plant/attack_sep/",
                        scale_mod=0.773, state="idle"
                    )
                else:
                    enemy = False
                if enemy is not False:
                    # multiply the tile position by the tile size in pixels and scaling
                    enemy.center_x = cartesian[0] * GRID_PIXEL_SIZE
                    enemy.center_y = cartesian[1] * GRID_PIXEL_SIZE
                    # set the boundaries for the enemy to move between if exists
                    # ONLY DO BOUNDARIES FOR THOSE NOT COLLIDING WITH WALLS
                    # same concept of cartesian
                    if "boundary_left" in ene.properties:
                        bound_cart = self.tile_map.get_cartesian(
                            abs(ene.properties["boundary_left"] * TILE_SCALING), abs(ene.shape[1])
                        )
                        enemy.boundary_left = bound_cart[0] * GRID_PIXEL_SIZE
                    if "boundary_right" in ene.properties:
                        bound_cart = self.tile_map.get_cartesian(
                            abs(ene.properties["boundary_right"] * TILE_SCALING), abs(ene.shape[1])
                        )
                        enemy.boundary_right = bound_cart[0] * GRID_PIXEL_SIZE
                    # set the enemy x move speed to 1 to move it if running else idle
                    if enemy.state == "running":
                        enemy.change_x = ENEMY_SPEED
                    # add to scene
                    self.scene.add_sprite("Enemies", enemy)

        # load the items for the level
        if "Items" in self.tile_map.object_lists:
            items_layer = self.tile_map.object_lists["Items"]
            for i in items_layer:
                cartesian = self.tile_map.get_cartesian(
                    abs(i.shape[0]), abs(i.shape[1])
                )
                item_type = i.properties["name"]
                if item_type == "health":
                    item = Item(
                        item_type, ITEM_SCALING, SPRITE_NATIVE_SIZE, GUI_SCALING, UPDATES_PER_FRAME,
                        "assets/Items/apple/", "assets/Items/collect/"
                    )
                else:
                    item = False
                if item is not False:
                    # multiply the tile position by the tile size in pixels and scaling
                    item.center_x = cartesian[0] * GRID_PIXEL_SIZE
                    item.center_y = cartesian[1] * GRID_PIXEL_SIZE
                    self.scene.add_sprite("Items", item)

        # start the physics engine
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITY,
            walls=self.scene["Terrain"]
        )

        # create the cameras here
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # center camera on user
        self.pan_camera_to_user()

        # set bg color
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        self.clear()
        # select the camera that will be moving with the player
        self.camera.use()
        self.scene.draw()

        # select the camera that will be drawing the static ui
        self.camera_gui.use()

        # draws the hearts and weapons gui
        self.heart_list.draw()
        self.weapon_gui_list.draw()


    # resize the camera's dimensions to show bigger/smaller part of screen
    def on_resize(self, width, height):
        # resize window that doesn't really look good at the moment
        # pass resizable = True into window var to enable
        self.camera.resize(width, height)

    # standard user input code
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.player.jump_sound)

        elif key == arcade.key.A:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player.change_x = MOVEMENT_SPEED

        # for pause, 'P' key
        # self -> to preserve your game state
        elif key == arcade.key.P:
            pause = PauseView(self)
            self.window.show_view(pause)


    # i press left to go left
    # i press right to right
    # i release left and my character stops moving
    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            if self.player.change_x < 0:
                self.player.change_x = 0
        elif key == arcade.key.D:
            if self.player.change_x > 0:
                self.player.change_x = 0

    def pan_camera_to_user(self, panning_fraction=1.0):
        self.screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        self.screen_center_y = 0
        if self.screen_center_x < 0:
            self.screen_center_x = 0
        elif self.screen_center_x >= self.end_of_map - self.camera.viewport_width:
            self.screen_center_x = self.end_of_map - self.camera.viewport_width
        user_centered = self.screen_center_x, self.screen_center_y
        self.camera.move_to(user_centered, panning_fraction)
        self.camera.use()

    def on_update(self, delta_time):
        if not self.game_over:
            if self.player.center_x >= self.end_of_map:
                if self.level < self.max_level:
                    self.going = True
                    self.level += 1
                    self.load_level(self.level)
                # reached max_level, you want to display GameOver
                else:
                    self.window.show_view(GameOverView(self))

            if self.player.center_x <= 0:
                if self.level > 1:
                    self.going = False
                    self.level -= 1
                    self.load_level(self.level)

            # check if the player fell off map
            if self.player.center_y < -100:
                self.player.center_x = 1 * GRID_PIXEL_SIZE
                self.player.center_y = 1 * GRID_PIXEL_SIZE


            # handling enemies and updating if they exist
            if "Enemies" in self.tile_map.object_lists:
                for enemy in self.scene["Enemies"]:
                    # If the enemy hit a wall, reverse
                    if len(arcade.check_for_collision_with_list(enemy, self.scene["Terrain"])) > 0:
                        enemy.change_x *= -1
                    if len(arcade.check_for_collision_with_list(enemy, self.scene["Enemies"])) > 0:
                        enemy.change_x *= -1

                # check if PLAYER has collided with the enemy
                if len(arcade.check_for_collision_with_list(self.player, self.scene["Enemies"])) > 0:
                    self.scene = self.player.take_damage(self.scene, self.heart_list)
                    if self.scene.game_over is True:
                        self.window.show_view(GameOverView(self))

                # update the enemies animation
                self.scene.update_animation(delta_time, ["Enemies"])
                # update enemies themselves
                self.scene.update(
                    ["Enemies"]
                )

                # handle enemy hitting boundary to reverse direction.
                for enemy in self.scene["Enemies"]:
                    # delete enemies that are off the map
                    if enemy.right < 0 or enemy.left > self.end_of_map:
                        enemy.remove_from_sprite_lists()
                    if (
                            enemy.boundary_right
                            and enemy.right > enemy.boundary_right
                            and enemy.change_x > 0
                    ):
                        enemy.change_x *= -1

                    if (
                            enemy.boundary_left
                            and enemy.left < enemy.boundary_left
                            and enemy.change_x < 0
                    ):
                        enemy.change_x *= -1


            # Check if Traps exist on the tilemap
            # If so, check if player has collided with them
            if "Traps" in self.tile_map.sprite_lists:
                if len(arcade.check_for_collision_with_list(self.player, self.scene["Traps"])) > 0:
                    self.scene = self.player.take_damage(self.scene, self.heart_list)
                    if self.scene.game_over is True:
                        self.window.show_view(GameOverView(self))

            # handling items and updating them if they exist
            if "Items" in self.tile_map.object_lists:
                pickup_list = arcade.check_for_collision_with_list(self.player, self.scene["Items"])
                for item in pickup_list:
                    # collected marks object for removal and plays removal animation
                    item.collected = True
                    # handle item pickup and item adding to inventory here (create function)
                    if item.collect_wait == 0:
                        arcade.play_sound(self.player.collect_item)
                        self.player, self.heart_list = item.run_behavior(
                            self.player, self.heart_list
                        )
                # update the items animation
                self.scene.update_animation(delta_time, ["Items"])
                # update items
                self.scene.update(
                    ["Items"]
                )

            # updating movement and environment
            # Update Animations
            self.scene.update_animation(
                delta_time,
                [
                    "Terrain",
                    "Player",
                ],
            )

            self.physics_engine.update()

            # move the camera and pan to user
            self.pan_camera_to_user(panning_fraction=0.12)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # 1. Create StartMenu object
    # 2. Initialize it with game view
    game_view = MyGame(MUSIC_PATH)
    start_menu = MenuView(game_view)

    # 3. show view is called on the Start Menu object
    window.show_view(start_menu)

    # 4. on_draw method of StartMenu called continuously
    arcade.run()

main()