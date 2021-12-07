def rename_right(command, files_names, change):
    """Removes or add characters from/to right"""
    if command == 'rm':
        new_names = [name[:len(name) - int(change)] for name in files_names]
    elif command == 'add':
        new_names = [name + change for name in files_names]
    return new_names


def rename_left(command, files_names, change):
    """Removes or add characters from/to left"""
    if command == 'rm':
        new_names = [name[int(change):] for name in files_names]
    elif command == 'add':
        new_names = [change + name for name in files_names]
    return new_names


def rename_position(command, files_names, change, position):
    """Removes or add characters at position"""
    if command == 'rm':
        new_names = [name[:int(position)] + name[int(position) + int(change):]
                     for name in files_names]
    elif command == 'add':
        new_names = [name[:int(position)] + change + name[int(position):]
                     for name in files_names]
    return new_names


def rename_replace(mode, files_names, before, after):
    """Replace one string to another"""
    new_names = []
    if mode == 'A':
        new_names = [name.replace(before, after) for name in files_names]
    elif mode == 'F':
        for name in files_names:
            position = name.find(before)
            tmp = name[position:position + len(after)].replace(before, after)
            new_names.append(name[:position] + tmp + name[position + 1:])
    elif mode == 'L':
        for name in files_names:
            position = name.rfind(before)
            tmp = name[position:position + len(after)].replace(before, after)
            new_names.append(name[:position] + tmp + name[position + 1:])
    return new_names
