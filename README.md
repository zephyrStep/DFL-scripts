# DFL Helper Scripts
Goal: to allow management of multiple workspaces with the existing DFL batch scripts and work flow with minimal extra work

# Setup


### Config
Create a file called `config.ini` inside the config directory (same level as settings.py).

For example this is my .ini setup
```ini
[Directory]
WORKSPACES_BASE = H:\MVE\space\workspaces
INTERNAL_PATH = H:\MVE\space\_internal
```

WORKSPACES_BASE: Root of workspaces you will be managing.
INTERNAL_PATH: Path to DFL `_internal` folder.
