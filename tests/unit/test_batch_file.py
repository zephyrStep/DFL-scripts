from pathlib import Path

from unittest.mock import Mock, call

from scripts import set_active_workspace
from scripts.set_active_workspace import set_workspace, get_workspace_batch_file_location


def test_expected_file_contents_are_written(patch_open, mock_config, monkeypatch):
    monkeypatch.setattr(set_active_workspace, get_workspace_batch_file_location.__name__, Mock())
    workspace_base = 'some_workspace_base'
    mock_config.WORKSPACES_BASE = Path(workspace_base)

    target = 'test'
    expected = fr"SET WORKSPACE={workspace_base}\{target}" + "\\"

    set_workspace(target)
    file_mock = patch_open.file

    assert file_mock.write.call_args_list[0] == call(expected)

