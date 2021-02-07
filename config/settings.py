import configparser
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from utils.paths import get_logs_dir

config = None


def setup_logging():
    cfg = get_config()
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)

    file = cfg.LOG_LOCATION / 'workspaces.log'
    file_handler = RotatingFileHandler(file, maxBytes=cfg.LOG_MAX_BYTES, backupCount=cfg.LOG_BACKUP_COUNT)
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(cfg.LOG_LEVEL)

    stream_formatter = logging.Formatter('%(levelname)s - %(message)s')
    file_formatter = logging.Formatter('[%(asctime)s] %(module)s.%(funcName)s-%(lineno)d [%(levelno)s] - %(message)s')

    file_handler.setFormatter(file_formatter)
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.debug("Logger initialized")


def get_base_config_path():
    return Path(__file__).parent / 'config.ini'


def get_config_path() -> Path:
    if os.environ.get("SCRIPTS_CONFIG_PATH"):
        path = Path(os.environ.get("SCRIPTS_CONFIG_PATH"))
    else:
        path = get_base_config_path()

    return path


class Config:
    WORKSPACES_BASE: Path
    INTERNAL_PATH: Path
    LOG_LOCATION: Path
    LOG_SIZE_IN_MB: int
    LOG_BACKUP_COUNT: int
    LOG_LEVEL: str

    def __init__(self, workspaces_base, internal_path, log_location, log_max_bytes, log_backup_count, log_level):
        self.WORKSPACES_BASE = workspaces_base
        self.INTERNAL_PATH = internal_path
        self.LOG_LOCATION = log_location
        self.LOG_MAX_BYTES = log_max_bytes
        self.LOG_BACKUP_COUNT = log_backup_count
        self.LOG_LEVEL = log_level


def _load_config():
    config_file = get_config_path()

    parser = configparser.ConfigParser()
    parser.read(config_file)

    workspace_loc = Path(parser.get('Directory', 'WORKSPACES_BASE'))
    internal_loc = Path(parser.get('Directory', 'INTERNAL_PATH', fallback=workspace_loc.parent))
    log_location = Path(parser.get('Logging', 'LOG_LOCATION', fallback=get_logs_dir()))
    log_max_bytes = int(parser.getint('Logging', 'LOG_SIZE_IN_MB', fallback=20) * (1000*1000))
    log_backup_count = parser.getint('Logging', 'LOG_BACKUP_COUNT', fallback=2)
    log_level = parser.get('Logging', 'LOG_LEVEL', fallback=logging.INFO)

    return Config(workspaces_base=workspace_loc,
                  internal_path=internal_loc,
                  log_location=log_location,
                  log_max_bytes=log_max_bytes,
                  log_backup_count=log_backup_count,
                  log_level=log_level
                  )


def get_config() -> Config:
    global config

    if not config:
        config = _load_config()

    return config
