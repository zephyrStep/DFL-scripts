import argparse
from pathlib import Path
import re

IMAGE_EXT = ['jpg','png']

def parse_args():
    parser = argparse.ArgumentParser(description='Rename files in the target directory to remove extra prefixes/suffixes leaving only the numeric portion')

    parser.add_argument('debug_folder', help='Path to debug folder')

    args = parser.parse_args()

    return args

def choose_segment(parts: list):
    """Return a purely numeric filename for aligned_debug

    Split a filename at each _ pick a purely numeric segment to use as the name. If none are purely numeric,
    use the entire name but replace all non-numeric characters.
    """
    numeric_segment = list(filter(lambda seg: seg.isnumeric(), parts))

    if numeric_segment:
        chosen = numeric_segment[0]
    else:
        chosen = re.sub('\D', '', "".join(parts))

    # assert chosen
    return chosen


def run(args):
    target = Path(args.debug_folder)
    print(f'target path: {target}')
    assert target.is_dir()

    for file in target.iterdir():
        if file.suffix[1:] in IMAGE_EXT:
            new_stem = choose_segment(file.stem.split('_'))

            new_path = Path(file).parent / (new_stem + file.suffix)

            try:
                file.rename(new_path)
            except FileExistsError as e:
                print(f'File {new_path.name} exists, removing {file.name} instead')
                file.unlink()


if __name__ == '__main__':
    run(parse_args())