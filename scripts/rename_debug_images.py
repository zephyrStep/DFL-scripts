import argparse
import logging
from pathlib import Path
import re

from utils.prompts import prompt_agree

IMAGE_EXT = ['jpg', 'png']

logger = logging.getLogger('main')


def choose_segment(parts: list):
    """Get the image number from a debug image"

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


def move_landmark_debug_images(source: Path, dest: Path, rename=True, test=True):
    """Moves all debug images from an _aligned folder into its corresponding aligned_debug folder

    :param source: Input directory containing landmark _debug images mixed with regular aligned
    :param dest: Folder to move the debug images to
    """
    assert source.is_dir()

    logger.info(f'Moving debug images in {source} to {dest}')
    for file in source.iterdir():
        if 'debug' in file.stem and file.suffix[1:] in IMAGE_EXT:
            if rename:
                new_stem = choose_segment(file.stem.split('_'))
            else:
                new_stem = file.stem

            new_path = dest / (new_stem + file.suffix)

            if test:
                logger.info(f'old: {file} new: {new_path}')
                continue

            try:
                file.rename(new_path)
            except FileExistsError as e:
                print(f'File {new_path.name} exists, removing {file.name} instead')
                file.unlink()


def run(source: Path, dest: Path, rename: bool, test: bool):
    logger.info(f"This will move all debug images in: {source}")
    logger.info(f"Into {dest}")
    logger.info(f"Files will be renamed: {rename}")

    if prompt_agree("Is this correct?"):
        move_landmark_debug_images(source, dest, rename, test)

