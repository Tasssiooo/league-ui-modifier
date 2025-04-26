import sys
import tkinter as tk

from tkinter import filedialog
from pathlib import Path
from configparser import ConfigParser
from .fs import RELATIVE_PATH


CONFIG_FILE = RELATIVE_PATH / "config.ini"


def get_league_folder_path() -> Path:

    config = ConfigParser()
    config.read(CONFIG_FILE)

    if (
        not CONFIG_FILE.exists()
        or not config.has_section("General")
        or not config.has_option("General", "leagueFolderPath")
        or not config.get("General", "leagueFolderPath")
    ):
        root = tk.Tk()
        root.withdraw()

        league_folder_path = filedialog.askdirectory(
            title="Select your League folder path",
        )

        if not league_folder_path:
            print("You must set the path of your League folder!!!")
            sys.exit(1)

        if not config.has_section("General"):
            config.add_section("General")

        config.set("General", "leaguefolderpath", league_folder_path)
        config.write(CONFIG_FILE.open("w"))

    return Path(config.get("General", "leagueFolderPath"))


def get_cslol_folder_path() -> Path:

    config = ConfigParser()
    config.read(CONFIG_FILE)

    if (
        not config.has_section("General")
        or not config.has_option("General", "cslolFolderPath")
        or not config.get("General", "cslolFolderPath")
    ):
        root = tk.Tk()
        root.withdraw()

        cslol_folder_path = filedialog.askdirectory(
            title="Select your cslol folder path",
        )

        if not cslol_folder_path:
            print("You must set the path of your cslol-manager!!!")
            sys.exit(1)

        if not config.has_section("General"):
            config.add_section("General")

        config.set("General", "cslolFolderPath", cslol_folder_path)
        config.write(CONFIG_FILE.open("w"))

    return Path(config.get("General", "cslolFolderPath"))
