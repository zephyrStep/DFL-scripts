import builtins
from unittest.mock import Mock

import pytest

import config
from config import Config
from config import get_config



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
    monkeypatch.setattr(config, Config.__name__, Mock(return_value=mock))
    monkeypatch.setattr(config, config.load_config.__name__, Mock(return_value=mock))

    cfg = get_config()

    return cfg