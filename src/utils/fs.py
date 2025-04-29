import os
import json
import shutil
import sys

from pathlib import Path
from tkinter import filedialog
from typing import IO


RELATIVE_PATH = Path(sys.executable).parent


def make_meta_info(
    dst: Path, author: str, description: str, name: str, version: str
) -> None:

    info_file = (dst / "info.json").open("w")

    json.dump(
        {
            "Author": author,
            "Description": description,
            "Name": name,
            "Version": version,
        },
        info_file,
    )


def copy_assets(src: Path, dst: Path) -> None:

    if not os.path.exists(src):

        raise FileNotFoundError(f"Source not found: {src}")

    shutil.copytree(src, dst, dirs_exist_ok=True)


def get_mod_file() -> IO:

    file = filedialog.askopenfile(
        title="Select the file of the mod you want to update",
        filetypes=(
            ("fantome files", "*.fantome"),
            ("zip files", "*.zip"),
            ("WAD files", "*.wad.client"),
        ),
    )

    if not file:
        print("You must select the file of the mod you want to update!")
        sys.exit(1)

    return file
