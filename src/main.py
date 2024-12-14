import sys
import json
import re

from pathlib import Path


RE_ENTRIES = re.compile(r"\n    (?=\")")
RE_HASH = re.compile(
    r"\"[\w/]+\"\s(?==)"
)  # To ignore the scenes: \"[\w/]+(_\w+)+\"\s(?==)


def update(scheme: dict[str, dict[str, str]], entry: str) -> str:
    """
    Modifies the entry according to the scheme, then returns a str.
    """

    def recursive(value, key: str, entry: str):

        if key in value:
            for k, v in value[key].items():
                if isinstance(v, str):
                    if re.search(k, entry):
                        entry = re.sub(rf"{k}.*(?=\n)", v, entry)
                    else:
                        splited_entry = entry.split("\n")
                        splited_entry.insert(-1, f"    	{v}")
                        entry = "\n".join(splited_entry)
                elif k in entry_hash:
                    entry = recursive(value[key], k, entry)

        return entry

    entry_hash = RE_HASH.search(entry)

    if entry_hash:
        entry_hash = entry_hash.group()
    else:
        input(
            f"Error: Hash not found! This file isn't well formatted!\nPress enter to exit..."
        )
        sys.exit(1)

    entry_type, _ = entry_hash.split("/")[-2:]

    return recursive(scheme, entry_type, entry)


def scheme_resolver() -> dict[str, dict[str, str]]:
    """
    Asks if the user wants to use a custom scheme.

    If so, it searches for a user specified .json file in the scheme folder, then returns it.
    Otherwise, it returns the default scheme.
    """
    while True:
        scheme_name = "default.json"

        match input("Do you want to use a custom scheme? [y/n]: ").lower():
            case "y" | "yes":
                scheme_name = Path(input("Scheme name: ")).with_suffix(".json")

            case "n" | "no":
                print("Using default scheme...")
            case _:
                continue

        try:
            with open(f"deps/schemes/{scheme_name}", "r") as scheme_json:
                return json.load(scheme_json)
        except FileNotFoundError:
            input(f"Error: {scheme_name} not found!\nPress enter to exit...")
            sys.exit(1)
        except json.JSONDecodeError as e:
            input(
                f"Error: Your json file is bad formatted.\n{e.msg}\nPress enter to exit..."
            )
            sys.exit(1)


def main(argv: list[str]) -> None:
    for i in range(len(argv)):
        arg = argv[i]

        try:
            with open(arg, "r") as uibase:
                # Checks if the file probably has a bin format;
                if uibase.readline() == "#PROP_text\n":
                    outname = Path(arg).with_suffix(".mod.py")
                    scheme = scheme_resolver()

                    uibase_content = uibase.read()
                    uibase_entries = RE_ENTRIES.split(uibase_content)

                    # 'entries' is formatted as a map (map[hash, embed]), that pattern allows us
                    # to split the uibase content using '\n    (?=\")' and iterate through them;
                    for i in range(1, len(uibase_entries)):
                        entry = uibase_entries[i]

                        uibase_entries[i] = update(scheme, entry)

                    with open(outname, "w") as uibase_mod:
                        uibase_entries.insert(0, "#PROP_text")
                        uibase_mod.write("\n".join(uibase_entries))

                else:
                    print(f"Error: {arg} probably doesn't have a bin format!")

                    if i == len(argv) - 1:
                        input("Press enter to exit...")
                        sys.exit(1)

        except FileNotFoundError:
            print(f"Error: {arg} not found!")

            if i == len(argv) - 1:
                input("Press enter to exit...")
                sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
