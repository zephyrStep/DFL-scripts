import argparse
import os
from pathlib import Path
from typing import List

from config.settings import get_config
from scripts import get_scripts_root

SET_SPACE_FILENAME = 'set_workspace.bat'

def get_workspace_choices() -> List[Path]:
    config = get_config()

    workspaces = config.WORKSPACES_BASE.iterdir()

    return [space for space in workspaces if space.is_dir()]


def get_batch_file_location() -> Path:
    config = get_config()

    internal = config.INTERNAL_PATH

    return internal / SET_SPACE_FILENAME


def set_workspace(choice):
    config = get_config()

    batch_file = get_batch_file_location()

    relative_path = config.WORKSPACES_BASE / choice
    scripts_dir = get_scripts_root()

    workspace_env = f"SET WORKSPACE={relative_path}{os.sep}"
    scripts_env = f"SET WORKSPACE_SCRIPTS={scripts_dir}{os.sep}"

    with open(batch_file, 'w') as file:
        file.write(workspace_env)
        file.write(os.linesep)
        file.write(scripts_env)


def parse_workspace_choice():
    parser = argparse.ArgumentParser("Set the current workspace for use by the DFL batch scripts")

    choices = list(map(lambda path: path.stem, get_workspace_choices()))
    parser.add_argument('workspace', choices=choices)

    args = parser.parse_args()

    return args.workspace


def run():
    choice = parse_workspace_choice()
    set_workspace(choice)

if __name__ == '__main__':
    run()