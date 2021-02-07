from pathlib import Path
import config
import scripts


def get_scripts_root():
    return Path(scripts.__file__).parent


def get_project_root():
    return get_scripts_root().parent


def get_config_dir():
    return Path(config.__file__).parent


def get_resources_dir():
    return get_project_root() / 'resources'


def get_logs_dir():
    return get_resources_dir() / 'logs'
