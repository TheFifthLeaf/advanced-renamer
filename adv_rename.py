import os
import sys
import argparse as arps

import operations as opr


def parser():
    """Parses given arguments"""
    arg_parser = arps.ArgumentParser(
        usage="adv-renamer [--help] {add,rm,replace}",
        description="Advanced Renamer makes sorting a large number of files much easier.",
        epilog="To see more information please use: adv-renamer <command> --help",
    )
    subparsers = arg_parser.add_subparsers(
        dest="command"
    )
    add_parser = subparsers.add_parser(
        "add",
        usage="adv-renamer add [--help] [path mode arguments]",
        description="Add given text to files names",
        help="Add given text to files names",
        epilog="Modes:\t\tArguments:\n"
               "R (right)\ttext\n"
               "L (left)\ttext\n"
               "B (both)\ttext\n"
               "P (position)\ttext number",
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
        usage="adv-renamer rm [--help] [path mode arguments]",
        description="Remove number of characters from files names",
        help="Remove number of characters from files names",
        epilog="Modes:\t\tArguments:\n"
               "R (right)\ttext\n"
               "L (left)\ttext\n"
               "B (both)\ttext\n"
               "P (position)\ttext number",
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
        usage="adv-renamer replace [--help] [path mode arguments]",
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


def main(command, path, mode, arguments):

    if command in ('add', 'rm'):

        try:
            os.chdir(path)
        except FileNotFoundError:
            print('Invalid path')
            main()

        try:
            files_old = list(os.walk(path))[0][2]
            if len(files_old) == 0:
                raise Exception
        except Exception:
            print('There are no files in the path')
            main()

        nm_old, extensions = opr.separate(files_old)

        if command == 'remove':
            try:
                change = int(float(inp[3]))
            except IndexError:
                print('Insufficient number of parameters')
                main()
            try:
                if change <= 0:
                    raise Exception
            except Exception:
                print('The remove number must be greater then zero')
                main()
        elif command == 'add':
            try:
                change = inp[3]
            except IndexError:
                print('Insufficient number of parameters')
                main()
            try:
                chars = ['*', ':', '<', '>', '?', '/', '\\', '|', '\"']
                for x in chars:
                    if x in change:
                        raise Exception
            except Exception:
                print('Invalid characters entered')
                main()

        if mode == '-r':
            nm_new = opr.right(command, nm_old, change)
        elif mode == '-l':
            nm_new = opr.left(command, nm_old, change)
        elif mode == '-b':
            nm_new = opr.left(command, opr.right(command, nm_old, change), change)
        elif mode == '-p':
            try:
                inner_position = int(float(inp[4]))
            except IndexError:
                print('Insufficient number of parameters')
                main()
            try:
                if inner_position < 0:
                    raise Exception
            except Exception:
                print('The position number must be greater then or equal to zero')
                main()
            nm_new = opr.position(command, nm_old, change, inner_position)
        else:
            print('Undefined command')

        files_new = opr.join(nm_new, extensions)

        opr.rename(files_old, files_new)

    elif command == 'replace':

        try:
            path, mode, before, after = inp[1], inp[2], inp[3], inp[4]
        except IndexError:
            print('Insufficient number of parameters')
            main()

        try:
            chars = ['*', ':', '<', '>', '?', '/', '\\', '|', '\"']
            for x in chars:
                if x in before:
                    raise Exception
        except Exception:
            print('Invalid characters entered')
            main()
        try:
            chars = ['*', ':', '<', '>', '?', '/', '\\', '|', '\"']
            for x in chars:
                if x in after:
                    raise Exception
        except Exception:
            print('Invalid characters entered')
            main()

        try:
            os.chdir(path)
        except FileNotFoundError:
            print('Invalid path')
            main()

        try:
            files_old = list(os.walk(path))[0][2]
            if len(files_old) == 0:
                raise Exception
        except Exception:
            print('There are no files in the path')
            main()

        nm_old, extensions = opr.separate(files_old)

        if mode in ('-a', '-f', '-l'):
            nm_new = opr.replace(mode, nm_old, before, after)
        else:
            print('Undefined command')

        files_new = opr.join(nm_new, extensions)

        opr.rename(files_old, files_new)

    elif command == 'help':

        print('''
README

Remove from:
    right:  remove -files- -r -num_of_chars-
    left:   remove -files- -l -num_of_chars-
    both:   remove -files- -b- -num_of_chars-
    posit:  remove -files- -p- -num_of_chars- -pos-
    eg:     remove "D:\\Video" -p 6 8

Add to:
    right:  add -files- -r -txt-
    left:   add -files- -l -txt-
    both:   add -files- -b- -txt-
    posit:  add -files- -p- -txt- -pos-
    eg:     add "D:\\Video" -p "[2020]" 8

Replace:
    all:    replace -files- -a -old- -new-
    first:  replace -files- -f -old- -new-
    last:   replace -files- -l -old- -new-
    eg:     replace "D:\\Video" -a "[2020]" "-2021-"

To exit:
    exit

To display help:
    help
''')

    elif command == 'exit':

        sys.exit()

    else:

        print('Undefined command')


if __name__ == '__main__':

    try:
        main(*parser())
    except Exception:
        print('An unknown error has occurred:')
        print(sys.exc_info())
