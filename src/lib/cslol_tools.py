import subprocess

from pathlib import Path
from utils.fs import RELATIVE_PATH


WAD_MAKE = RELATIVE_PATH / "deps" / "cslol_tools" / "wad-make.exe"
WAD_EXTRACT = RELATIVE_PATH / "deps" / "cslol_tools" / "wad-extract.exe"

HASHDICT = RELATIVE_PATH / "deps" / "hashes" / "hashes.game.txt"


def cslol_wad_make(src: Path, dst: Path) -> Path:

    subprocess.run([WAD_MAKE, src, dst])

    return dst


def cslol_wad_extract(src: Path, dst: Path) -> None:

    wad_extract_exe = subprocess.run([WAD_EXTRACT, src, dst, HASHDICT])
