import argparse

import scripts
from config.settings import setup_logging
from scripts.set_active_workspace import get_workspace_choices


setup_logging()

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers()

p = subparsers.add_parser('choose_workspace', help="Set the current workspace for use by the DFL batch scripts")


def run_choose_workspace(args):
    scripts.set_active_workspace.choose_workspace()


p.set_defaults(func=run_choose_workspace)


def bad_args(arguments):
    parser.print_help()
    exit(0)


parser.set_defaults(func=bad_args)

arguments = parser.parse_args()
arguments.func(arguments)

