import argparse
import logging

from destination import ImplicitDestination
from categorizer import Lootorganizer
from fs_handler import NopMoveImpl, FileMoveImpl


def parse_args() -> argparse.Namespace:
    """
    Parses the arguments given to the program.
    :return: parsed Namespace with the arguments.
    """
    parser = argparse.ArgumentParser(prog="lootorganizer")
    parser.add_argument("--depth", dest="depth", type=int, default=2,
                        help="How many levels to descend to the file system hierachy")
    parser.add_argument("-n", "--dry-run", dest="dry_run", action="store_true",
                        help="Don't actually perform file operations, just print what would be done")
    parser.add_argument("incoming", action="store", help="Incoming folder containing the unorganized files")
    parser.add_argument("target", help="Folder to move the organized files to")

    return parser.parse_args()


def setup_logging(debug=False) -> None:
    """ Sets up the logging. """
    loglevel = logging.INFO
    if debug:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel, format="%(levelname)s\t %(message)s")


def main() -> None:
    args = parse_args()
    setup_logging()

    file_move_strategy = None
    if args.dry_run:
        file_move_strategy = NopMoveImpl()
    else:
        file_move_strategy = FileMoveImpl()

    dest_impl = ImplicitDestination(args.target)
    loot = Lootorganizer(args.incoming, dest_impl=dest_impl, file_handler=file_move_strategy)
    loot.examinate_target()
