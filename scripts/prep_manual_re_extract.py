import logging
import shutil
from pathlib import Path
from typing import List

from scripts.create_new_workspace import MANUAL_EXTRACT
from scripts.rename_debug_images import IMAGE_EXT
from utils.prompts import prompt_confirm

logger = logging.getLogger('main')


def get_unique_image_stems_from_dir(path: Path) -> set:
    return {img.stem for img in filter(lambda file: file.suffix[1:] in IMAGE_EXT, path.iterdir())}


def get_images_from_dir(path: Path) -> List[Path]:
    return [img for img in filter(lambda file: file.suffix[1:] in IMAGE_EXT, path.iterdir())]


def find_deleted_images(deleted_dir, original_dir) -> set:

    deleted_dir_images_names = get_unique_image_stems_from_dir(deleted_dir)

    original_image_names = get_unique_image_stems_from_dir(original_dir)

    deleted_names = original_image_names - deleted_dir_images_names

    logger.info(f"Detected {len(deleted_names)} images deleted from debug")

    return deleted_names


def copy_frames_of_deleted_faces(original_dir: Path, extract_dir: Path, deleted_names: set):
    """Copy the original frames from any deleted faces into the extract dir"""

    logger.info(f"Copying frames of faces deleted from debug dir into extract dir: {extract_dir}")
    original_images = get_images_from_dir(original_dir)
    for image in original_images:
        if image.stem in deleted_names:
            copy_path = extract_dir / image.name
            shutil.copy(image, copy_path)


def remove_faces_from_aligned_matching_deleted(aligned_dir: Path, deleted_names: set):
    """Delete images"""
    logger.info("Removing faces from aligned that were deleted in _debug")
    aligned_faces = get_images_from_dir(aligned_dir)
    face_count = 0
    for image in aligned_faces:
        # split since aligned has _0,_1 and we just need the image number
        stem = image.stem.split('_')
        if stem[0] in deleted_names:
            face_count += 1
            image.unlink()

    logger.info(f"Removed {face_count} faces matching the deleted debug frames")


def prep_for_manual_extraction(frames_dir: Path, aligned_dir: Path, debug_dir: Path, extract_dir=None):

    if not extract_dir:
        extract_dir = frames_dir / MANUAL_EXTRACT
        logger.info(f"No extract dir provided, using default: {extract_dir}")
        extract_dir.mkdir(exist_ok=True)
    else:
        logger.info(f"Manual extract dir set to: {extract_dir}")

    if prompt_confirm("\nYou are about to delete all aligned images that were deleted from _debug. "
                      "Only do this if you are sure your debug folder is not missing any extra images.\n"
                      "Continue?"):

        deleted_names = find_deleted_images(deleted_dir=debug_dir, original_dir=frames_dir)
        copy_frames_of_deleted_faces(original_dir=frames_dir, extract_dir=extract_dir, deleted_names=deleted_names)
        remove_faces_from_aligned_matching_deleted(aligned_dir=aligned_dir, deleted_names=deleted_names)
