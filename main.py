import argparse
import os
from pathlib import Path

import scripts
from config.settings import setup_logging
from scripts import rename_debug_images
from scripts.prep_manual_re_extract import prep_for_manual_extraction
from scripts.set_active_workspace import get_workspace_choices


setup_logging()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


class FixPathAction(argparse.Action):
    # thanks DFL
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, Path(os.path.abspath(os.path.expanduser(values))))


def run_choose_workspace(args):
    scripts.set_active_workspace.choose_workspace(show_workspace=args.show_workspace)


p = subparsers.add_parser('choose_workspace', help="Set the current workspace for use by the DFL batch scripts")
p.add_argument('--show_workspace', help='Prints the currently active workspace', action='store_true')
p.set_defaults(func=run_choose_workspace)


def run_move_landmark_debug(args):
    rename_debug_images.run(img_base=args.image_base,
                            aligned_dir=args.source,
                            debug_dir=args.dest,
                            rename=args.rename,
                            test=args.test)


p = subparsers.add_parser('move_landmark_debug', help="Move landmark debug images from source to dest")
p.add_argument('-i', '--image-base', required=True, action=FixPathAction, dest='image_base')
p.add_argument('-s', '--source', required=True, action=FixPathAction, dest='source')
p.add_argument('-d', '--dest', required=True, action=FixPathAction, dest='dest')
p.add_argument('-r', '--rename-off', dest='rename', action='store_false',
               help='Dont rename debug images, default is to rename')
p.add_argument('-t', '--test', action='store_true')

p.set_defaults(func=run_move_landmark_debug)


def run_prep_reextract(args):
    prep_for_manual_extraction(frames_dir=args.image_base,
                               aligned_dir=args.aligned_dir,
                               debug_dir=args.debug_dir,
                               extract_dir=args.extract_dir)
    pass


p = subparsers.add_parser('prep_re_extract', help='Use after deleting images from _debug. To prep for re-extract')
p.add_argument('--image-base', required=True, action=FixPathAction, dest='image_base', help='folder containing video frames')
p.add_argument('--aligned-dir', required=True, action=FixPathAction, dest='aligned_dir', help='Aligned directory')
p.add_argument('--debug-dir', required=True, action=FixPathAction, dest='debug_dir',
               help='Aligned debug folder youve deleted faces from')
p.add_argument('--manual-extract-dir', required=False, action=FixPathAction, dest='extract_dir',
               help="Folder to place frames into to for re-extraction")

p.set_defaults(func=run_prep_reextract)


def bad_args(arguments):
    parser.print_help()
    exit(0)


parser.set_defaults(func=bad_args)

arguments = parser.parse_args()
arguments.func(arguments)

