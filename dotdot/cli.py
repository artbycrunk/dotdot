import os
from argparse import ArgumentParser

import dotdot

def parser():
    parser = ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "-c", "--config-file", dest="config_file", help="Use this config file"
    )
    parser.add_argument(
        "-d",
        "--dotfiles-dir",
        dest="base_dir",
        help="The dotfiles dir to work on",
        metavar="BASEDIR",
    )
    parser.add_argument(
        "--plugin-dir",
        action="append",
        dest="plugin_dirs",
        default=[],
        metavar="PLUGIN_DIR",
        help="load all plugins in PLUGIN_DIR",
    )
    parser.add_argument(
        "--no-color",
        dest="no_color",
        action="store_true",
        help="Disable colored output",
    )
    parser.add_argument("--version", action="store_true")

    args = parser.parse_args()
    return args
