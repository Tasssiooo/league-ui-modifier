import subprocess
import requests

from pathlib import Path
from utils.fs import RELATIVE_PATH


RITOBIN_CLI = RELATIVE_PATH / "deps" / "ritobin" / "ritobin_cli.exe"

HASHES_DIR = RELATIVE_PATH / "deps" / "hashes"

COMMUNITY_DRAGON_HASHTABLE = (
    "https://github.com/CommunityDragon/Data/raw/master/hashes/lol/hashes.{}.txt"
)


def fetch_hashtables():

    print("Downloading hashtables...")

    if not HASHES_DIR.exists():
        HASHES_DIR.mkdir()

    names = ["binentries", "binfields", "binhashes", "bintypes", "lcu", "rst", "game"]

    for name in names:
        hash_file = HASHES_DIR / f"./hashes.{name}.txt"

        if name == "game":
            for n in range(2):
                hash_file = HASHES_DIR / "hashes.game.txt"

                if hash_file.exists():
                    hash_file.unlink()

                r = requests.get(COMMUNITY_DRAGON_HASHTABLE.format(name) + f".{n}")

                with open(HASHES_DIR / "hashes.game.txt", "a") as hashes_game_txt:
                    hashes_game_txt.write(r.content.decode("utf-8"))
            break

        r = requests.get(COMMUNITY_DRAGON_HASHTABLE.format(name))

        with open(hash_file, "w") as hashes_x_txt:
            hashes_x_txt.write(r.content.decode("utf-8"))

            print(f"{hash_file.name} downloaded")

    print("Hashtables downloading finished!\n")


def ritobin_cli(src: Path, dst: Path, outype: str):

    ritobin_cli_exe = subprocess.run(
        [RITOBIN_CLI, src, dst, "-o", outype, "-d", HASHES_DIR],
    )

    if not ritobin_cli_exe.returncode:
        return dst.open("r+")
