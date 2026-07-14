import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent
OUTPUT_FOLDER_PATH = ASSETS_DIR.parent / "pack"
PACK_MAKER_PATH = ASSETS_DIR / "PackMaker.exe"
IGNORE_FOLDERS = {
	"__pycache__",
	"tools",
	"zz_ignore_old",
}


def discover_pack_folders(assets_dir=ASSETS_DIR):
    assets_dir = Path(assets_dir)
    return sorted(
        path
        for path in assets_dir.iterdir()
        if path.is_dir()
        and not path.name.startswith(".")
        and path.name.casefold() not in IGNORE_FOLDERS
    )


def pack_folder(
    folder_path,
    pack_maker_path=PACK_MAKER_PATH,
    output_folder_path=OUTPUT_FOLDER_PATH,
):
    folder_path = Path(folder_path).resolve()
    pack_maker_path = Path(pack_maker_path).resolve()
    output_folder_path = Path(output_folder_path).resolve()

    if not folder_path.is_dir():
        print(f'Error: Folder "{folder_path}" does not exist', file=sys.stderr)
        return False

    if not pack_maker_path.is_file():
        print(f'Error: PackMaker executable "{pack_maker_path}" does not exist', file=sys.stderr)
        return False

    output_folder_path.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(
            [
                str(pack_maker_path),
                "--input",
                folder_path.name,
                "--output",
                str(output_folder_path),
            ],
            check=True,
            cwd=folder_path.parent,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Error occurred while packing {folder_path.name}: {error}", file=sys.stderr)
        return False

    return True



def pack_all_folders(assets_dir=ASSETS_DIR):
    all_folders = discover_pack_folders(assets_dir)
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(pack_folder, all_folders))

    return all(results)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Pack folders for the game.")
    parser.add_argument("folder_name", nargs="?", help="The name of the folder to pack")
    parser.add_argument("--all", action="store_true", help="Pack all folders")

    args = parser.parse_args(argv)

    if args.all and args.folder_name:
        parser.error("folder_name and --all cannot be used together")
    if args.all:
        success = pack_all_folders()
    elif args.folder_name:
        folder_path = Path(args.folder_name)
        if not folder_path.is_absolute():
            folder_path = ASSETS_DIR / folder_path
        success = pack_folder(folder_path)
    else:
        parser.error("provide a folder name or use --all")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
