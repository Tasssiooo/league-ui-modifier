import sys

from pathlib import Path
from tkinter import filedialog


RELATIVE_PATH = Path(sys.executable).parent


def get_mod_filename() -> Path:

    file = filedialog.askopenfilename(
        title="Select the file of the mod you want to update",
        filetypes=(
            ("fantome files", "*.fantome"),
            ("zip files", "*.zip"),
            ("WAD files", "*.wad.client"),
        ),
    )

    if not file:
        input(
            "You must select the file of the mod you want to update!\nPress Enter to exit..."
        )
        sys.exit(1)

    return Path(file)
