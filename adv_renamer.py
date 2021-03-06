import os
import sys
import argparse as arps

import operations as opr


def parser():
    """Parses given arguments"""
    arg_parser = arps.ArgumentParser(
        usage=os.path.basename(__file__) + " [--help] {add,rm,replace} [path mode arguments]",
        description="Advanced Renamer makes sorting a large number of files much easier.",
        epilog="To see more information please use: adv-renamer <command> --help",
    )
    subparsers = arg_parser.add_subparsers(
        dest="command"
    )
    add_parser = subparsers.add_parser(
        "add",
        usage=f"{os.path.basename(__file__)} add [--help] [path mode arguments]",
        description="Add given text to files names",
        help="Add given text to files names",
        epilog="Modes:\t\tArguments:\n"
               "R (right)\ttext\n"
               "L (left)\ttext\n"
               "B (both)\ttext\n"
               "P (position)\ttext position",
        formatter_class=arps.RawTextHelpFormatter
    )
    add_parser.add_argument(
        "path",
        type=str,
        metavar="path",
        help="Directory of files to rename"
    )
    add_parser.add_argument(
        "mode",
        type=str,
        choices=["R", "L", "B", "P"],
        metavar="mode",
        help="Script behaviour while adding"
    )
    add_parser.add_argument(
        "arguments",
        type=str,
        nargs="+",
        metavar="arguments",
        help="Parameters required by the specified mode"
    )
    rm_parser = subparsers.add_parser(
        "rm",
        usage=f"{os.path.basename(__file__)} rm [--help] [path mode arguments]",
        description="Remove number of characters from files names",
        help="Remove number of characters from files names",
        epilog="Modes:\t\tArguments:\n"
               "R (right)\tnumber\n"
               "L (left)\tnumber\n"
               "B (both)\tnumber\n"
               "P (position)\tnumber position",
        formatter_class=arps.RawTextHelpFormatter
    )
    rm_parser.add_argument(
        "path",
        type=str,
        metavar="path",
        help="Directory of files to rename"
    )
    rm_parser.add_argument(
        "mode",
        type=str,
        choices=("R", "L", "B", "P"),
        metavar="mode",
        help="Script behaviour while removing"
    )
    rm_parser.add_argument(
        "arguments",
        type=str,
        nargs="+",
        metavar="arguments",
        help="Parameters required by the specified mode"
    )
    replace_parser = subparsers.add_parser(
        "replace",
        usage=f"{os.path.basename(__file__)} replace [--help] [path mode arguments]",
        description="Replace old string with the new one in files names",
        help="Replace old string with the new one in files names",
        epilog="Modes:\t\tArguments:\n"
               "F (first)\ttext_old text_new\n"
               "L (last)\ttext_old text_new\n"
               "A (all)\t\ttext_old text_new",
        formatter_class=arps.RawTextHelpFormatter
    )
    replace_parser.add_argument(
        "path",
        type=str,
        metavar="path",
        help="Directory of files to rename"
    )
    replace_parser.add_argument(
        "mode",
        type=str,
        choices=("F", "L", "A"),
        metavar="mode",
        help="Script behaviour while removing"
    )
    replace_parser.add_argument(
        "arguments",
        type=str,
        nargs="+",
        metavar="arguments",
        help="Parameters required by the specified mode"
    )
    args = arg_parser.parse_args()
    return (args.command, args.path, args.mode, args.arguments)


def check_string(text):
    """checks if the string contains forbidden in path characters"""
    forbidden_chars = {'*', ':', '<', '>', '?', '/', '\\', '|', '\"'}
    if len(forbidden_chars.intersection(text)) > 0:
        sys.exit("Forbidden chars in the new path")


def main(command, path, mode, arguments):
    """The main function of the program that control and performs all the actions."""

    path = os.path.normpath(path)
    path = os.path.abspath(path)

    if os.path.exists(path) is False:
        sys.exit("Entered path does not exists")

    if os.path.isfile(path):
        path_files = [path]
    elif os.path.isdir(path):
        path_files = list(os.walk(path))[0][2]

    if len(path_files) <= 0:
        sys.exit("No files in the path")

    if command == "add":
        check_string(arguments[0])
    elif command == "replace":
        check_string(arguments[1])

    files = [path_file.replace(path_file, path + "\\" + path_file) for path_file in path_files]
    files_names = [os.path.splitext(path_file)[0] for path_file in path_files]
    files_extensions = [os.path.splitext(path_file)[1] for path_file in path_files]

    if command in ("add", "rm"):
        if mode == "R":
            new_names = opr.rename_right(command, files_names, arguments[0])
        elif mode == "L":
            new_names = opr.rename_left(command, files_names, arguments[0])
        elif mode == "B":
            new_names = opr.rename_left(command, opr.rename_right(command, files_names, arguments[0]), arguments[0])
        elif mode == "P":
            new_names = opr.rename_position(command, files_names, arguments[0], arguments[1])
    elif command == "replace":
        new_names = opr.rename_replace(mode, files_names, arguments[0], arguments[1])

    new_files = [name + extension for name, extension in zip(new_names, files_extensions)]
    new_files = [new_file.replace(new_file, path + "\\" + new_file) for new_file in new_files]

    for file, new_file in zip(files, new_files):
        os.rename(file, new_file)


if __name__ == '__main__':

    try:
        main(*parser())
    except Exception:
        print('An unknown error has occurred:')
        print(sys.exc_info())
