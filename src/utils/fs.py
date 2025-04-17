import os
import json
import shutil
import sys

from pathlib import Path


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
