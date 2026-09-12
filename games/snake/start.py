#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
from engine.controls import get_menu_back
from engine.controls import get_menu_confirm
from engine.controls import get_menu_navigation
from games.snake.visuals import draw_snake_menu
#-----------------------------


#=============================#
# SNAKE ACTIONS               #
#=============================#
#-----------------------------
ACTION_BACK = "BACK"
#-----------------------------


#=============================#
# SNAKE MENU CONFIG           #
#=============================#
#-----------------------------
MENU_ITEMS = [
    "PLAY",
    "OPTIONS",
    "BACK",
]
#-----------------------------


#=============================#
# SNAKE GAME                  #
#=============================#
#-----------------------------
class SnakeGame:
    def __init__(self):
        self.selected_index = 0

    def update(self, events):
        navigation = get_menu_navigation(
            events
        )

        self.selected_index = (
            self.selected_index + navigation
        ) % len(MENU_ITEMS)

        if get_menu_back(
            events
        ):
            return ACTION_BACK

        if get_menu_confirm(
            events
        ):
            selected_item = MENU_ITEMS[
                self.selected_index
            ]

            if selected_item == "BACK":
                return ACTION_BACK

        return None

    def draw(self, surface):
        draw_snake_menu(
            surface,
            MENU_ITEMS,
            self.selected_index
        )
#-----------------------------


#=============================#
# GAME FACTORY                #
#=============================#
#-----------------------------
def create_game():
    return SnakeGame()
#-----------------------------