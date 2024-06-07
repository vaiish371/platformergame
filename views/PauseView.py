import arcade
import arcade.gui
from views.MenuView import MenuView
class PauseView(arcade.View):
    # game_view : MyGame object which returns the current game state/view
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()
        # vertical box to wrap the buttons in
        self.v_box = arcade.gui.UIBoxLayout()

    # triggered automatically when we call window.show_view
    def on_show_view(self):

        # UIManager to handle the UI.
        self.manager.enable()

        # set background color
        arcade.set_background_color(arcade.color.DARK_SKY_BLUE)

        # Resume Game
        # Restart Game
        # Go back to Main Menu

        # Creating Buttons
        resume_button = arcade.gui.UIFlatButton(text="Resume Game", width= 300)
        restart_button = arcade.gui.UIFlatButton(text="Restart Game", width= 300)
        menu_button = arcade.gui.UIFlatButton(text="Go back to Main Menu", width= 300)

        # Adding them into vertical box
        self.v_box.add(resume_button.with_space_around(bottom=20))

        self.v_box.add(restart_button.with_space_around(bottom=20))
        self.v_box.add(menu_button.with_space_around(bottom=20))

        # wrap the vertical box and center its elements
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x = "center_x",
                anchor_y = "center_y",
                child=self.v_box
            )
        )

        # Define callbacks to add functionality when buttons are pressed
        resume_button.on_click = self.on_click_resume
        restart_button.on_click = self.on_click_restart
        menu_button.on_click = self.on_click_menu

    def on_hide_view(self):
        self.manager.disable()


    def on_click_resume(self, event):
        self.clear()
        print("Resume:", event)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.window.show_view(self.game_view)

    # If the person presses 'P' when in pause menu
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.P:
            arcade.set_background_color(arcade.color.SKY_BLUE)
            self.window.show_view(self.game_view)

    def on_click_restart(self, event):
        self.clear()
        print("Restart:", event)
        self.game_view.setup()
        self.window.show_view(self.game_view)

    def on_click_menu(self, event):
        self.clear()
        print("Return menu:", event)
        self.window.show_view(MenuView(self.game_view))

    def on_draw(self):
        self.clear()
        self.manager.draw()


