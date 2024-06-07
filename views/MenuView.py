import arcade
import arcade.gui


class MenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

    def on_show_view(self):

        # UIManager to handle the UI.
        self.manager.enable()

        # set background color
        arcade.set_background_color(arcade.color.DARK_SKY_BLUE)

        # create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        # assign self.on_click_start as callback
        start_button.on_click = self.on_click_start
        quit_button.on_click = self.on_click_quit

        # create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_hide_view(self):
        self.manager.disable()

    def on_click_quit(self, event):
        print("Quit: ", event)
        arcade.exit()

    def on_click_start(self, event):
        print("Game Start: ", event)
        self.game_view.setup()
        self.window.show_view(self.game_view)

    def on_draw(self):
        self.window.clear()
        self.manager.draw()
