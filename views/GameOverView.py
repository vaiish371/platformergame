import arcade
import arcade.gui

from views.MenuView import MenuView

class GameOverView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()
        # vertical box to wrap the buttons in
        self.v_box = arcade.gui.UIBoxLayout()

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(arcade.color.DARK_SKY_BLUE)

        ui_text_label = arcade.gui.UILabel(
            text="Game Over",
            width = 200,
            font_size = 24,
            font_name="Arial",
            text_color=arcade.color.BROWN
        )

        self.v_box.add(ui_text_label.with_space_around(bottom=20))

        # Restart
        # Main Menu

        # create the buttons
        restart_button = arcade.gui.UIFlatButton(text="Restart Game", width=200)
        self.v_box.add(restart_button.with_space_around(bottom=20))

        menu_button = arcade.gui.UIFlatButton(text="Main Menu", width=200)
        self.v_box.add(menu_button.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box
            )
        )

        restart_button.on_click = self.on_click_restart
        menu_button.on_click = self.on_click_menu


    def on_hide_view(self):
        self.manager.disable()

    def on_click_restart(self, event):
        print("Restarting game...", event)
        self.game_view.setup()
        self.window.show_view(self.game_view)


    def on_click_menu(self, event):
        print("Returning to main menu", event)
        self.window.show_view(MenuView(self.game_view))

    def on_draw(self):
        self.clear()
        self.manager.draw()