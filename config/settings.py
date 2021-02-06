import configparser
import os
from dataclasses import dataclass
from pathlib import Path


config = None


def get_base_config_path():
    return Path(__file__).parent / 'config.ini'


def get_config_path() -> Path:
    if os.environ.get("SCRIPTS_CONFIG_PATH"):
        path = Path(os.environ.get("SCRIPTS_CONFIG_PATH"))
    else:
        path = get_base_config_path()

    return path

@dataclass
class Config:

    WORKSPACES_BASE: Path
    INTERNAL_PATH: Path


def load_config():
    config_file = get_config_path()

    parser = configparser.ConfigParser()
    parser.read(config_file)

    workspace_loc = Path(parser.get('Directory', 'WORKSPACES_BASE'))
    internal_loc = Path(parser.get('Directory', 'INTERNAL_PATH', fallback=workspace_loc.parent))

    return Config(WORKSPACES_BASE=workspace_loc,
                  INTERNAL_PATH=internal_loc
                  )



def get_config() -> Config:
    global config

    if not config:
        config = load_config()

    return config