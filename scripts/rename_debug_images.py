import argparse
import logging
import shutil
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


def copy_missing_base_images_into_debug(base_image_dir: Path, debug_dir: Path):
    debug_images_names = {img.stem for img in filter(lambda file: file.suffix[1:] in IMAGE_EXT, debug_dir.iterdir())}
    logger.info(f'{len(debug_images_names)} debug images found')
    base_image_paths = [img for img in filter(lambda file: file.suffix[1:] in IMAGE_EXT, base_image_dir.iterdir())]
    logger.info(f'{len(base_image_paths)} base images found')
    logger.info(f'Finding missing images')

    missing = []
    for img in base_image_paths:
        if img.stem not in debug_images_names:
            missing.append(img)

    logger.info(f'Copying {len(missing)} missing files into debug')
    for img in missing:
        copy_path = debug_dir / img.name
        shutil.copy(img, copy_path)


def run(img_base: Path, aligned_dir: Path, debug_dir: Path, rename: bool, test: bool):
    logger.info(f"This will move all debug images in: {aligned_dir}")
    logger.info(f"Into {debug_dir}")
    logger.info(f"Files will be renamed: {rename}")

    if prompt_agree("Is this correct?"):
        move_landmark_debug_images(aligned_dir, debug_dir, rename, test)
        copy_missing_base_images_into_debug(base_image_dir=img_base, debug_dir=debug_dir)


