#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
from importlib import import_module
#-----------------------------


#=============================#
# GAME LOADING                #
#=============================#
#-----------------------------
def create_game(game_entry):
    if not game_entry.playable:
        return None

    start_module = import_module(
        game_entry.start_module
    )

    create_game_function = getattr(
        start_module,
        "create_game",
        None
    )

    if not callable(
        create_game_function
    ):
        raise ValueError(
            f"Game '{game_entry.game_id}' "
            f"has no valid create_game() function."
        )

    game = create_game_function()

    if not callable(
        getattr(
            game,
            "update",
            None
        )
    ):
        raise ValueError(
            f"Game '{game_entry.game_id}' "
            f"has no valid update() method."
        )

    if not callable(
        getattr(
            game,
            "draw",
            None
        )
    ):
        raise ValueError(
            f"Game '{game_entry.game_id}' "
            f"has no valid draw() method."
        )

    return game
#-----------------------------