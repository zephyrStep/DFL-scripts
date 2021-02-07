import json
import logging
from copy import deepcopy
from pathlib import Path

logger = logging.getLogger('main')

WORKSPACE_SETTINGS_FILE = 'workspace_settings.json'
DEFAULT_SETTINGS = 'defaults.json'

internal_settings = None


def default_settings():
    return {
        'scripts_env_key': 'WORKSPACE_SCRIPTS',
        'autosave': True,
        'dfl_workspace_key': "WORKSPACE"
    }


class InternalSettings:

    def __init__(self):
        self._settings_path = Path(__file__).parent / WORKSPACE_SETTINGS_FILE
        self._settings_json = default_settings()
        self._settings_json.update(self._load_settings())
        self._settings_from_load = deepcopy(self._settings_json)

    def _load_settings(self):
        """Load settings from the file, or create the file if it does not yet exist"""

        if not self._does_settings_file_exist():
            return self._initialize_settings_file()

        with open(self._settings_path, 'r') as f:
            contents = f.read()
        logger.debug(f'Loaded from settings file: {contents}')
        try:
            settings = json.loads(contents)
        except json.JSONDecodeError as e:
            settings = {}
        return settings

    def _initialize_settings_file(self) -> dict:
        """Create the settings file from default settings, overwriting any value that existed"""
        logger.debug("Creating settings file")

        defaults = default_settings()
        logger.debug(f'Loaded defaults {defaults}')

        content = json.dumps(defaults)
        logger.debug(f"Writing {content} to settings file: {self._settings_path}")
        with open(self._settings_path, 'w') as f:
            f.write(content)

        return defaults

    def _does_settings_file_exist(self) -> bool:
        return self._settings_path.exists()

    def _save_settings(self):
        """Save currently loaded settings to disk"""
        logger.debug("Saving settings...")
        self._settings_from_load.update(self._settings_json)

        logger.debug(self._settings_from_load)
        with open(self._settings_path, 'w') as f:
            f.write(json.dumps(self._settings_from_load))

    def _do_autosave(self):
        """Save the current settings if autosaving is turned on"""
        if self.autosave:
            self._save_settings()

    def _update_setting(self, key, value):
        """Update a setting and autosave"""
        self._settings_json[key] = value
        self._do_autosave()

    @property
    def current_workspace(self) -> str:
        return self._settings_json.get('current_workspace')

    @current_workspace.setter
    def current_workspace(self, value: str):
        self._update_setting('current_workspace', value)

    @property
    def autosave(self) -> bool:
        return self._settings_json.get('autosave')

    @autosave.setter
    def autosave(self, value: bool):
        self._update_setting('autosave', value)

    @property
    def scripts_env_key(self) -> str:
        return self._settings_json.get('scripts_env_key')

    @property
    def dfl_workspace_key(self) -> str:
        return self._settings_json.get('dfl_workspace_key')



def get_internal_settings():

    global internal_settings

    if not internal_settings:
        internal_settings = InternalSettings()

    return internal_settings
