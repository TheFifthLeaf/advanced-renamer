# Advanced Renamer

Advanced Renamer makes sorting a large number of files much easier.

## Installation

This program uses only the standard Python 3 library, so installing additional modules is not necessary.

## Usage

Run:

```bash
python adv_rename.py
```

Remove from:

```bash
remove [path] [mode] [num_of_chars] [pos_if_pos_mode]
```

Add to:

```bash
add [path] [mode] [string] [pos_if_pos_mode]
```

Replace:

```bash
replace [path] [mode] [old_string] [new_string]
```

For help:

```bash
help
```

For exit:

```bash
exit
```

## Available modes

For "remove" and "add":

```bash
# Right: -r
add "D:\Video" -r "-2021"
remove "D:\Video" -r 5

# Left: -l
add "D:\Video" -l "april_"
remove "D:\Video" -l 6

# Both: -b
add "D:\Video" -b "--"
remove "D:\Video" -b 2

# Positional: -p
add "D:\Video" -p "_office_" 7
remove "D:\Video" -p 8 7
```

For "replace":

```bash
# All matches: -a
replace "D:\Video" -a "2020" "2021"

# First match: -f
replace "D:\Video" -f "." "-"

# Last match: -l
replace "D:\Video" -f "-" "."
```

## Contributing

Pull requests are welcome.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)