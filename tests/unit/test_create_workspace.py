from scripts.create_new_workspace import get_base_workspaces_path


def test_get_workspaces_base_returns_cfg_value(mock_config):
    expected = 'test123'
    mock_config.WORKSPACES_BASE = expected

    result = get_base_workspaces_path()

    assert result == expected
