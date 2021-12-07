import os


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

    if mode == 'rm':
        for x in old:
            nm.append(x[:len(x) - int(chng)])
    elif mode == 'add':
        for x in old:
            nm.append(x + chng)

    return nm


def left(mode, old, chng):
    # Removes or add characters from/to left

    nm = []

    if mode == 'rm':
        for x in old:
            nm.append(x[int(chng):])
    elif mode == 'add':
        for x in old:
            nm.append(chng + x)

    return nm


def position(mode, old, chng, pos):
    # Removes or add characters at position

    nm = []

    if mode == 'rm':
        for x in old:
            nm.append(x[:int(pos)] + x[int(pos) + int(chng):])
    elif mode == 'add':
        for x in old:
            nm.append(x[:int(pos)] + chng + x[int(pos):])

    return nm


def replace(mode, old, bef, aft):
    # Replace one string to another

    nm = []

    if mode == 'A':
        for x in old:
            nm.append(x.replace(bef, aft))
    elif mode == 'F':
        for x in old:
            pos = x.find(bef)
            tmp = x[pos:pos + len(aft)].replace(bef, aft)
            nm.append(x[:pos] + tmp + x[pos + 1:])
    elif mode == 'L':
        for x in old:
            pos = x.rfind(bef)
            tmp = x[pos:pos + len(aft)].replace(bef, aft)
            nm.append(x[:pos] + tmp + x[pos + 1:])

    return nm
