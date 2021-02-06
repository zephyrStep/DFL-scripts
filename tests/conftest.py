import builtins
from pathlib import Path
from unittest.mock import Mock

import pytest

import config.settings as settings
from config.settings import Config, get_config, load_config



class OpenMock(Mock):
    file = Mock()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __enter__(self):
        return self.file

    def __exit__(self, *args):
        pass

@pytest.fixture
def patch_open(monkeypatch):
    open_mock = OpenMock()
    monkeypatch.setattr(builtins, 'open', OpenMock)

    return open_mock

@pytest.fixture
def mock_config(monkeypatch):
    """Patch get_config and return the mock it returns."""
    mock = Mock()
    monkeypatch.setattr(settings, Config.__name__, Mock(return_value=mock))
    monkeypatch.setattr(settings, load_config.__name__, Mock(return_value=mock))

    cfg = get_config()

    return cfg

@pytest.fixture
def patch_path_mkdir(monkeypatch):
    mkdir_mock = Mock()
    monkeypatch.setattr(Path, 'mkdir', Mock(return_value=mkdir_mock))

    return mkdir_mock