import os
import subprocess
import sys
from pathlib import Path

import pytest

from config.settings import get_config
from scripts.set_active_workspace import get_batch_file_location


def test_command_sets_env():

    pytest.mark.skipif(not sys.platform.startswith('win32'))
    assert os.getenv('WORKSPACE') is None

    batch_file = get_batch_file_location()
    batch_command = batch_file.read_text()
    cmd = f'cmd /V /C "{batch_command}&& ECHO !WORKSPACE!'
    out = subprocess.check_output(cmd, shell=True)
    out = out.decode('utf-8').strip()
    print(out)

    config = get_config()
    assert Path(out).parent == config.WORKSPACES_BASE