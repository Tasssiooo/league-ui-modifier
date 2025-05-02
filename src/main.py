import questionary
import tkinter as tk

from lib.ritobin import fetch_hashtables
from lib.modding import update_from_zip, update_from_wad
from utils.configuration import get_league_folder_path, get_cslol_folder_path
from utils.fs import get_mod_filename


MODS_BY_CATEGORY: dict[str, dict[str, dict[str, str]]] = {
    "Health Bar": {
        "Season 3 Health Bar": {
            "author": "Xllwd",
            "description": "15.something",
            "version": "5.4",
            "scheme": "season3healthbar.json",
            "uibase": "clientstates/gameplay/ux/lol/lolfloatinginfobars/uibase",
        },
    },
    "Loading Screen": {},
    "Shop": {},
    "Scoreboard": {},
    "Settings": {},
    "Ability Bar": {},
}


def main() -> None:

    root = tk.Tk()
    root.withdraw()

    if get_league_folder_path() and get_cslol_folder_path():

        fetch_hashtables()

        category = questionary.select(
            "What UI part do you want to modify?",
            choices=[category for category in MODS_BY_CATEGORY],
        ).ask()

        name = questionary.select(
            "What scheme do you want to use?",
            choices=[name for name in MODS_BY_CATEGORY[category]],
        ).ask()

        mod_filename = get_mod_filename()

        root.destroy()

        selected_mod = MODS_BY_CATEGORY[category][name]

        match mod_filename.suffix:
            case ".fantome" | ".zip":
                update_from_zip(mod_filename, selected_mod)
            case ".wad.client":
                update_from_wad(mod_filename, selected_mod)

        input("The process has finished successfully!\nPress Enter to exit...")


if __name__ == "__main__":
    main()
