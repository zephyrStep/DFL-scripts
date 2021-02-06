import argparse
import os
import sys
from pathlib import Path

from config import get_config

DATA_SRC = 'data_src'
DATA_DST = 'data_dst'

ALIGNED = 'aligned'
ALIGNED_DEBUG = 'aligned_debug'
ALIGNED_CONVERT = 'aligned_convert'

def get_workspace_structure():
    return {
        DATA_SRC: [ALIGNED],
        DATA_DST: [ALIGNED_CONVERT, ALIGNED_DEBUG, ALIGNED]
    }

def get_base_workspaces_path() -> Path:
    config = get_config()
    return config.WORKSPACES_BASE

def clear_directory(target: Path):
    # don't try to delete root!
    assert target != target.parent

    children = list(target.rglob("*"))
    # children

    response = input(
        f"{target} already exists, all {len(children)} files in this directory will be deleted. (Y|N)")
    if response != 'Y':
        print("Quitting")
        sys.exit()

    directories = []
    for child in children:
        if child.is_file():
            child.unlink()
        elif child.is_dir():
            directories.append(child)

    for directory in reversed(directories):
        directory.rmdir()


def create_workspace(workspace_name):
    base = get_base_workspaces_path()

    workspace_name = Path(workspace_name)
    new_workspace = base / workspace_name.name

    # ensure our target is a level below the base directory
    assert len(new_workspace.parts) > len(base.parts)

    if new_workspace.is_dir():
        clear_directory(new_workspace)
    if new_workspace.is_file():
        raise FileExistsError()

    new_workspace.mkdir(exist_ok=True)

    data_src = new_workspace / DATA_SRC
    data_dst = new_workspace / DATA_DST

    data_dst.mkdir()
    data_src.mkdir()

    project_structure = get_workspace_structure()

    for top_level_key in project_structure:
        sub_folders = project_structure[top_level_key]
        for folder in sub_folders:
            (new_workspace / top_level_key / folder).mkdir()

    print('Project structure created')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('workspace_name')
    create_workspace(parser.parse_args().workspace_name)
