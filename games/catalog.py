#=============================#
# IMPORTS                     #
#=============================#
#-----------------------------
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
#-----------------------------


#=============================#
# CATALOG CONFIG              #
#=============================#
#-----------------------------
GAMES_DIRECTORY = Path(
    __file__
).resolve().parent

REQUIRED_GAME_FILES = (
    "__init__.py",
    "meta.py",
    "start.py",
)

REQUIRED_META_FIELDS = (
    "title",
    "description",
)
#-----------------------------


#=============================#
# GAME ENTRY                  #
#=============================#
#-----------------------------
@dataclass(frozen=True)
class GameEntry:
    game_id: str
    title: str
    description: str
    start_module: str
#-----------------------------


#=============================#
# GAME DIRECTORY CHECK        #
#=============================#
#-----------------------------
def is_game_directory(directory):
    if not directory.is_dir():
        return False

    if directory.name.startswith("_"):
        return False

    for file_name in REQUIRED_GAME_FILES:
        if not (
            directory / file_name
        ).is_file():
            return False

    return True
#-----------------------------


#=============================#
# GAME META LOADING           #
#=============================#
#-----------------------------
def load_game_meta(game_id):
    if not game_id.isidentifier():
        raise ValueError(
            f"Invalid game directory name: "
            f"{game_id}"
        )

    meta_module = import_module(
        f"games.{game_id}.meta"
    )

    game_meta = getattr(
        meta_module,
        "GAME_META",
        None
    )

    if not isinstance(
        game_meta,
        dict
    ):
        raise ValueError(
            f"Game '{game_id}' has no valid "
            f"GAME_META dictionary."
        )

    for field in REQUIRED_META_FIELDS:
        if field not in game_meta:
            raise ValueError(
                f"Game '{game_id}' is missing "
                f"meta field '{field}'."
            )

        value = game_meta[field]

        if not isinstance(
            value,
            str
        ):
            raise ValueError(
                f"Meta field '{field}' in game "
                f"'{game_id}' must be a string."
            )

        if not value.strip():
            raise ValueError(
                f"Meta field '{field}' in game "
                f"'{game_id}' must not be empty."
            )

    return game_meta
#-----------------------------


#=============================#
# GAME CATALOG                #
#=============================#
#-----------------------------
def load_game_catalog():
    games = []

    for directory in GAMES_DIRECTORY.iterdir():
        if not is_game_directory(
            directory
        ):
            continue

        game_id = directory.name

        game_meta = load_game_meta(
            game_id
        )

        games.append(
            GameEntry(
                game_id=game_id,
                title=game_meta[
                    "title"
                ].strip(),
                description=game_meta[
                    "description"
                ].strip(),
                start_module=(
                    f"games.{game_id}.start"
                )
            )
        )

    games.sort(
        key=lambda game: (
            game.title.casefold(),
            game.game_id.casefold()
        )
    )

    return games
#-----------------------------