import os
import sys

import operations as opr


def input_slice(inp):
    # Slice elements from input

    pos, new_inp, index = 0, inp, []

    for x in inp:
        if x == '"':
            if len(index) == 0:
                index.append(pos)
            elif len(index) == 1:
                index.append(pos)
                old = inp[index[0] + 1:index[1]]
                new = inp[index[0] + 1:index[1]].replace(' ', '?')
                new_inp = inp.replace(old, new)
                index = []
        pos += 1

    new_inp = new_inp.replace('"', '').split()

    for x in range(len(new_inp)):
        new_inp[x] = new_inp[x].replace('?', ' ')

    return new_inp


def main():

    inp = input_slice(input('Enter command:'))

    try:
        command = inp[0]
    except IndexError:
        print('Please enter the command')
        main()

    if command in ('remove', 'add'):

        try:
            path, sub_command = inp[1], inp[2]
        except IndexError:
            print('Insufficient number of parameters')
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

        if sub_command == '-r':
            nm_new = opr.right(command, nm_old, change)
        elif sub_command == '-l':
            nm_new = opr.left(command, nm_old, change)
        elif sub_command == '-b':
            nm_new = opr.left(command, opr.right(command, nm_old, change), change)
        elif sub_command == '-p':
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
            path, sub_command, before, after = inp[1], inp[2], inp[3], inp[4]
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

        if sub_command in ('-a', '-f', '-l'):
            nm_new = opr.replace(sub_command, nm_old, before, after)
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
    while True:
        try:
            main()
        except Exception:
            print('An unknown error has occurred:')
            print(sys.exc_info())
