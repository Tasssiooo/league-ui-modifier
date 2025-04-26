import subprocess
import requests

from pathlib import Path
from utils.fs import RELATIVE_PATH


RITOBIN_CLI = RELATIVE_PATH / "deps" / "ritobin" / "ritobin_cli.exe"

COMMUNITY_DRAGON_HASHTABLE = (
    "https://github.com/CommunityDragon/Data/raw/master/hashes/lol/hashes.{}.txt"
)


def fetch_hashtables():

    names = ["binentries", "binfields", "binhashes", "bintypes", "lcu", "rst", "game"]

    for name in names:
        if name == "game":
            for n in range(2):
                r = requests.get(COMMUNITY_DRAGON_HASHTABLE.format(name) + f".{n}")

                with open("./hashes.game.txt", "a") as hashes_game_txt:
                    hashes_game_txt.write(r.content.decode("utf-8"))
            break

        r = requests.get(COMMUNITY_DRAGON_HASHTABLE.format(name))

        with open(f"./hashes.{name}.txt", "w") as hashes_x_txt:
            hashes_x_txt.write(r.content.decode("utf-8"))


def cslol_ritobin(src: Path, dst: Path):

    ritobin_cli_exe = subprocess.run(
        [
            "wine",
            RITOBIN_CLI,
            src,
            dst,
        ],
    )

    if not ritobin_cli_exe.returncode:
        return dst.open("r")


if __name__ == "__main__":
    fetch_hashtables()
