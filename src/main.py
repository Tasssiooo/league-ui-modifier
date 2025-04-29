import sys
import json
import re
import questionary
import shutil
import tkinter as tk

from lib.cslol_tools import cslol_wad_extract, cslol_wad_make
from lib.ritobin import cslol_ritobin, fetch_hashtables
from utils.configuration import get_league_folder_path, get_cslol_folder_path
from utils.fs import make_meta_info, copy_assets, get_mod_filename, RELATIVE_PATH


RE_ENTRIES = re.compile(r"\n    (?=\")")
RE_HASH = re.compile(
    r"\"[\w/]+\"\s(?==)"
)  # To ignore the scenes: \"[\w/]+(_\w+)+\"\s(?==)

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


def update(scheme: dict, entry: str) -> str:
    """
    Modifies the entry according to the scheme, then returns a str.
    """

    entry_hash = RE_HASH.search(entry)

    if entry_hash:
        entry_hash = entry_hash.group()
    else:
        input(
            f"Error: Hash not found! This file isn't well formatted!\nPress enter to exit..."
        )
        sys.exit(1)

    entry_type, _ = entry_hash.split("/")[-2:]

    def recursive(value: dict, key: str, entry: str):

        if key in value:
            for k, v in value[key].items():
                if isinstance(v, str):
                    if re.search(k, entry):
                        entry = re.sub(rf"{k}.*(?=\n)", v, entry)
                    else:
                        splited_entry = entry.split("\n")
                        splited_entry.insert(-1, f"    	{v}")
                        entry = "\n".join(splited_entry)
                elif re.search(k, entry_hash):
                    entry = recursive(value[key], k, entry)

        return entry

    return recursive(scheme, entry_type, entry)


def scheme_resolver(scheme: str) -> None:

    scheme_file = RELATIVE_PATH / "deps" / "schemes" / scheme

    try:
        return json.load(scheme_file.open("r"))
    except json.JSONDecodeError as e:

        input(
            f"Error: Your scheme file is bad formatted.\n{e.msg}\nPress enter to exit..."
        )

        sys.exit(1)


def main() -> None:

    root = tk.Tk()
    root.withdraw()

    fetch_hashtables()

    if get_league_folder_path() and get_cslol_folder_path():

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

        """ mod_dir = RELATIVE_PATH / name
        bin_dir = (mod_dir / selected_mod["uibase"]).parent

        uibase_bin = RELATIVE_PATH / "UI" / selected_mod["uibase"]
        uibase_dst = bin_dir / uibase_bin.with_suffix(".py").name

        if not uibase_bin.exists():

            cslol_wad_extract()

        uibase_py = cslol_ritobin(uibase_bin, uibase_dst)

        if not uibase_py:

            print("Something went wrong!")
            sys.exit(1)

        if not uibase_py.readline() == "#PROP_text\n":

            print("Bin file bad formatted!")
            sys.exit(1)

        scheme_dict = scheme_resolver(selected_mod["scheme"])

        uibase_content = uibase_py.read()
        uibase_entries = RE_ENTRIES.split(uibase_content)

        for i in range(1, len(uibase_entries)):

            entry = uibase_entries[i]

            uibase_entries[i] = update(scheme_dict, entry)

        uibase_py.close()

        with open(uibase_dst, "w") as uibase_mod:

            uibase_entries.insert(0, "#PROP_text")
            uibase_mod.write("\n".join(uibase_entries))

        uibase_mod_bin = cslol_ritobin(uibase_dst, uibase_dst.with_suffix(".bin"))

        if uibase_mod_bin:

            uibase_mod_bin.name.removesuffix(".bin")

        uibase_dst.unlink()

        copy_assets(RELATIVE_PATH / "deps" / "assets" / name, mod_dir)

        cslol_installed_dir = get_cslol_folder_path() / "installed"

        mod_pkg_name = name + " (by Xllwd)"
        mod_pkg_dir = cslol_installed_dir / mod_pkg_name
        mod_pkg_meta_dir = mod_pkg_dir / "META"
        mod_pkg_wad_dir = mod_pkg_dir / "WAD"

        if not mod_pkg_dir.exists():
            mod_pkg_dir.mkdir()
        if not mod_pkg_meta_dir.exists():
            mod_pkg_meta_dir.mkdir()
        if not mod_pkg_wad_dir.exists():
            mod_pkg_wad_dir.mkdir()

        make_meta_info(
            mod_pkg_meta_dir,
            selected_mod["author"],
            selected_mod["description"],
            name,
            selected_mod["version"],
        )

        cslol_wad_make(mod_dir, mod_pkg_wad_dir / "UI.wad.client")
        # Cleanup
        shutil.rmtree(mod_dir) """

        print("Done!")


if __name__ == "__main__":
    main()
