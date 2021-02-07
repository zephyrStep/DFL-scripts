import os
import shutil
from pathlib import Path

from utils.paths import get_project_root
from scripts.set_active_workspace import get_dfl_setenv_batch_file, SET_ENV_FILENAME, SET_SPACE_FILENAME, \
    get_workspace_batch_file_location

INIT_DONE_FILENAME = 'init_completed'


def setup_set_env_file(file_location: Path):
    """Append to DFL's set_env.bat to call our bat file"""
    with open(file_location, 'a') as f:
        f.write(f'{os.linesep}')
        f.write(f'call {SET_SPACE_FILENAME}')


def setup_batch_file():
    """Setup batch file that will add scripts to env"""
    print(f'Setting up {SET_SPACE_FILENAME}')
    batch_file = get_workspace_batch_file_location()
    scripts_root = get_project_root()

    scripts_env = f"SET WORKSPACE_SCRIPTS={scripts_root}"

    with open(batch_file, 'w') as file:
        file.write(scripts_env)


def init(force=False):

    # make sure DFLs setenv file is found
    setenv_file = get_dfl_setenv_batch_file()
    assert setenv_file.exists()


    with open(setenv_file, 'r') as f:
        contents = f.readlines()
    contents = filter(lambda line: SET_SPACE_FILENAME in line.strip(), contents)

    # Check that we haven't already configured the setenv file
    if list(contents) and not force:
        print(f'{SET_ENV_FILENAME} already configured.')
    else:
        print(f"Backing up {SET_ENV_FILENAME} before modifying it.")
        backup = setenv_file.parent / f'{setenv_file.name}.bak'
        shutil.copy(setenv_file, backup)

        print(f"Modifying DFL {SET_ENV_FILENAME} to add environment variables")
        setup_set_env_file(setenv_file)

    workspace_bat = get_workspace_batch_file_location()

    # Check if the workspace.bat is setup
    if not workspace_bat.exists() or force:
        print("Script env batch file doesn't exist, creating it now")
        setup_batch_file()
    else:
        with open(workspace_bat, 'r') as f:
            lines = f.readlines()
        if not list(filter(lambda line: 'WORKSPACE_SCRIPTS' in line, lines)):
            setup_batch_file()

    print("Done initializing.")


if __name__ == '__main__':
    init(force=True)




