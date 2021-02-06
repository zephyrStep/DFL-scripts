from pathlib import Path


def get_scripts_root():
    return Path(__file__).parent

def get_scripts_project_root():
    return get_scripts_root().parent