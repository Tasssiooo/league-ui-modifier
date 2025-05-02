import sys
import re
import json
import shutil

from zipfile import ZipFile
from pathlib import Path
from typing import Any

from cslol_tools import cslol_wad_extract, cslol_wad_make
from ritobin import ritobin_cli
from utils.fs import RELATIVE_PATH


RE_ENTRIES = re.compile(r"\n    (?=\")")
RE_HASH = re.compile(
    r"\"[\w/]+\"\s(?==)"
)  # To ignore the scenes: \"[\w/]+(_\w+)+\"\s(?==)


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


def get_scheme(scheme: str) -> Any:

    try:
        scheme_file = RELATIVE_PATH / "deps" / "schemes" / scheme

        return json.load(scheme_file.open("r"))
    except json.JSONDecodeError as e:
        input(
            f"Error: Your scheme file is bad formatted.\n{e.msg}\nPress Enter to exit..."
        )
        sys.exit(1)


def update_from_wad(wad: Path, mod: dict[str, str]) -> None:

    extracted_wad = wad.with_suffix("")

    cslol_wad_extract(wad, extracted_wad)

    wad.unlink()

    uibase_bin = extracted_wad / mod["uibase"]
    uibase_py = uibase_bin.with_suffix(".py")
    uibase_utf8 = ritobin_cli(uibase_bin, uibase_py, "text")

    uibase_bin.unlink()

    scheme = get_scheme(mod["scheme"])

    uibase_content = uibase_utf8.read()
    uibase_entries = RE_ENTRIES.split(uibase_content)

    for i in range(1, len(uibase_entries)):

        entry = uibase_entries[i]

        uibase_entries[i] = update(scheme, entry)

    uibase_utf8.write("\n".join(uibase_entries))
    uibase_utf8.close()

    uibase_bin = ritobin_cli(uibase_py, uibase_bin, "bin")
    uibase_bin.close()

    uibase_py.unlink()

    cslol_wad_make(extracted_wad, wad)

    shutil.rmtree(extracted_wad)


def update_from_zip(zip: Path, mod: dict[str, str]) -> None:

    unzipped = zip.with_suffix("")

    with ZipFile(zip, "r") as zip_ref:
        zip_ref.extractall(unzipped)

    wad = unzipped / "WAD" / "UI.wad.client"

    update_from_wad(wad, mod)
