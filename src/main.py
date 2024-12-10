import sys
import json

from pathlib import Path


def scheme_resolver() -> dict[str, str]:
    """
    Asks the user if he wants to use a custom scheme.

    If so, it searches for a user specified .json file in the scheme folder.
    Otherwise, it uses the default scheme.
    """
    while True:
        scheme_name = "default.json"

        match input("Do you want to use a custom scheme? [y/n]: "):
            case "y" | "Y":
                scheme_name = Path(input("Scheme name: ")).with_suffix(".json")

            case "n" | "N":
                print("Using default scheme...")

        try:
            with open(f"./schemes/{scheme_name}", "r") as scheme_json:
                return json.load(scheme_json)
        except FileNotFoundError:
            print(f"Error: {scheme_name} not found!")
            input("Press any key to exit...")
            sys.exit(1)


def main(argv: list[str]) -> None:
    for arg in argv:
        with open(arg, "r") as uibase:
            # Checks if the file probably has a bin format;
            if uibase.readline() == "#PROP_text\n":
                scheme = scheme_resolver()
                print(scheme)
            else:
                print("Error: This file probably doesn't have a bin format!")
                input("Press any key to exit...")


if __name__ == "__main__":
    main(sys.argv[1:])
