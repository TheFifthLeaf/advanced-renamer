import os
import sys


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


def separate(fls):
    # Separate names and extansions

    nm, ext = [], []

    for x in fls:
        nm.append(x[:x.rindex('.')])
        ext.append(x[x.rindex('.'):])

    return nm, ext


def join(new, ext):
    # Combine names with extensions

    fls = []

    for x in range(len(new)):
        fls.append(new[x] + ext[x])

    return fls


def rename(old, new):
    # Changes names of files

    for x in range(len(old)):
        os.rename(old[x], new[x])


def right(mode, old, chng):
    # Removes or add characters from/to right

    nm = []

    if mode == 'remove':
        for x in old:
            nm.append(x[:len(x) - chng])
    elif mode == 'add':
        for x in old:
            nm.append(x + chng)

    return nm


def left(mode, old, chng):
    # Removes or add characters from/to left

    nm = []

    if mode == 'remove':
        for x in old:
            nm.append(x[chng:])
    elif mode == 'add':
        for x in old:
            nm.append(chng + x)

    return nm


def position(mode, old, chng, pos):
    # Removes or add characters at position

    nm = []

    if mode == 'remove':
        for x in old:
            nm.append(x[:pos] + x[pos + chng:])
    elif mode == 'add':
        for x in old:
            nm.append(x[:pos] + chng + x[pos:])

    return nm


def replace(mode, old, bef, aft):
    # Replace one string to another

    nm = []

    if mode == '-a':
        for x in old:
            nm.append(x.replace(bef, aft))
    elif mode == '-f':
        for x in old:
            pos = x.find(bef)
            tmp = x[pos:pos + len(aft)].replace(bef, aft)
            nm.append(x[:pos] + tmp + x[pos + 1:])
    elif mode == '-l':
        for x in old:
            pos = x.rfind(bef)
            tmp = x[pos:pos + len(aft)].replace(bef, aft)
            nm.append(x[:pos] + tmp + x[pos + 1:])

    return nm


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

        nm_old, extensions = separate(files_old)

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
            nm_new = right(command, nm_old, change)
        elif sub_command == '-l':
            nm_new = left(command, nm_old, change)
        elif sub_command == '-b':
            nm_new = left(command, right(command, nm_old, change), change)
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
            nm_new = position(command, nm_old, change, inner_position)
        else:
            print('Undefined command')

        files_new = join(nm_new, extensions)

        rename(files_old, files_new)

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

        nm_old, extensions = separate(files_old)

        if sub_command in ('-a', '-f', '-l'):
            nm_new = replace(sub_command, nm_old, before, after)
        else:
            print('Undefined command')

        files_new = join(nm_new, extensions)

        rename(files_old, files_new)

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
