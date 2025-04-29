import subprocess

from pathlib import Path
from utils.configuration import get_league_folder_path
from utils.fs import RELATIVE_PATH


WAD_MAKE = RELATIVE_PATH / "deps" / "cslol_tools" / "wad-make.exe"
WAD_EXTRACT = RELATIVE_PATH / "deps" / "cslol_tools" / "wad-extract.exe"

HASHDICT = RELATIVE_PATH / "deps" / "hashes" / "hashes.game.txt"

UI_WAD = "Game/DATA/FINAL/UI.wad.client"


def cslol_wad_make(src: Path, dst: Path) -> Path:

    subprocess.run([WAD_MAKE, src, dst])

    return dst


def cslol_wad_extract() -> None:

    src = get_league_folder_path() / UI_WAD

    dst = RELATIVE_PATH / "UI"

    print("Extracting UI files...")

    wad_extract_exe = subprocess.run([WAD_EXTRACT, src, dst, HASHDICT])

    if not wad_extract_exe.returncode:

        print("UI files extracted succesfully!")
