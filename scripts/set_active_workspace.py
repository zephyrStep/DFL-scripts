import logging
import os
from pathlib import Path
from typing import List

from config.internal_settings import get_internal_settings
from config.settings import get_config
from utils.paths import get_project_root
from utils.prompts import prompt_choice

logger = logging.getLogger('main')

SET_SPACE_FILENAME = 'set_workspace.bat'
SET_ENV_FILENAME = 'setenv.bat'


def get_workspace_choices() -> List[Path]:
    config = get_config()

    workspaces = config.WORKSPACES_BASE.iterdir()

    return [space for space in workspaces if space.is_dir()]


def get_workspace_batch_file_location() -> Path:
    config = get_config()

    internal = config.INTERNAL_PATH

    return internal / SET_SPACE_FILENAME


def get_dfl_setenv_batch_file() -> Path:
    config = get_config()

    internal = config.INTERNAL_PATH

    return internal / SET_ENV_FILENAME


def set_workspace(choice):
    config = get_config()
    settings = get_internal_settings()

    batch_file = get_workspace_batch_file_location()

    relative_path = config.WORKSPACES_BASE / choice
    scripts_dir = get_project_root()

    workspace_env = f"SET {settings.dfl_workspace_key}={relative_path}"
    scripts_env = f"SET {settings.scripts_env_key}={str(scripts_dir)}"

    with open(batch_file, 'w') as file:
        file.write(workspace_env)
        file.write(os.linesep)
        file.write(scripts_env)

    internal_settings = get_internal_settings()
    internal_settings.current_workspace = choice
    logger.info(f"Current workspace changed to: {choice}")


def choose_workspace(show_workspace):
    settings = get_internal_settings()
    if show_workspace:
        logger.info(f"Current workspace: {settings.current_workspace}")
        return

    choices = list(map(lambda path: path.stem, get_workspace_choices()))

    logger.info(f"Current Workspace: {settings.current_workspace}")

    choice = prompt_choice("Select a workspace", choices)

    set_workspace(choice)


if __name__ == '__main__':
    choose_workspace('you_and_riley')
