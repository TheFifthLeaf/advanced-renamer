<h1 align="center">Advanced Renamer</h1>

<p align="center">The CLI script made with Python for sorting a large number of files much easier.</p>

<p  align="center">
	<a style="text-decoration:none" href="https://github.com/TheFifthLeaf/advanced-renamer/releases">
		<img src="https://img.shields.io/github/v/release/TheFifthLeaf/advanced-renamer?color=3C7DD9" alt="Releases">
	</a>
	<a style="text-decoration:none" href="https://www.python.org/downloads/">
		<img src="https://img.shields.io/badge/python-3.6%2B-3C7DD9" alt="Python Version">
	</a>
	<a style="text-decoration:none" href="https://choosealicense.com/licenses/gpl-3.0/">
		<img src="https://img.shields.io/badge/license-GPL%20V3-3C7DD9" alt="License GPLv3">
	</a>
	<a href="https://www.codefactor.io/repository/github/thefifthleaf/advanced-renamer">
		<img src="https://img.shields.io/codefactor/grade/github/TheFifthLeaf/advanced-renamer/main?color=3C7DD9" alt="CodeFactor" />
	</a>
</p>

## Installation

This program uses only the standard Python 3 library, so installing additional modules is not necessary.

## Usage

To rename using .exe, please type:

```bash
adv_renamer [--help] {add,rm,replace} [path mode arguments]
```

And using .py, type:

```bash
python adv_renamer.py [--help] {add,rm,replace} [path mode arguments]
```

### Usage example

This will display help information. You can also use short "-h".
```bash
adv_renamer --help
adv_renamer <command> --help
```
This will add string "_test_" to the end of the name of the file.
```bash
adv_renamer add "D\RandomFiles" R "_test_"
```
This will remove 6 characters from th end of the name of the file.
```bash
adv_renamer rm "D\RandomFiles" R 6
```
This will replace all matching strings from the name of the file with new one.
```bash
adv_renamer replace "D\RandomFiles" A "(1)" "[1]"
```
You can also add and remove characters to/from specific position.
```bash
adv_renamer add "D\RandomFiles" P "_test_" 3
adv_renamer rm "D\RandomFiles" P 6 3
```
If you want use string that start with "-" character, you should use "--" before.
```bash
adv_renamer add "D\RandomFiles" R -- "-test"
adv_renamer replace "D\RandomFiles" -- "-before" -- "--after"
```

## Supported modes

### add/rm
```bash
adv_renamer add path mode text <position>
adv_renamer rm path mode number <position>
```
- R (right)
- L (left)
- B (both)
- P (position)

### replace
```bash
adv_renamer replace path mode text_before text_after
```
- F (first)
- L (last)
- A (all)

## Contributing

Pull requests are welcome.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)