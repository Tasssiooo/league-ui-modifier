import subprocess

from pathlib import Path
from utils.fs import RELATIVE_PATH


RITOBIN_CLI = RELATIVE_PATH / "deps" / "ritobin" / "ritobin_cli.exe"


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
