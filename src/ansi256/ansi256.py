import argparse as _argparse
import pathlib as _pathlib
import tabulate as _tabulate

COLOR_CODE_FORMAT = "\033[{FGBG};5;{ID}m"
TABLE_FORMAT = "\033[{FGBG};5;{ID}m{ID:03d}"
SH_FORMAT="$'%{{\e[{FGBG};5;{ID}m%}}'"
TEST_FORMAT = "\033[{FGBG};5;{CODE}m"
RESET_FG = "\033[39m"
RESET_BG = "\033[49m"
FGBG_TO_CODE = {"fg": 38, "bg": 48}

COLS = 20
ROWS = 256 // COLS


def get_args():
    parser = _argparse.ArgumentParser(prog='ansi256', description='a tool for printing, testing, and exporting ansi color escapes')
    subparsers = parser.add_subparsers(required=True)
    pt_parser = subparsers.add_parser('print-table', help='print a table of the ansi color codes')
    pt_parser.add_argument('WHICH', choices=['fg','bg','both'], help='specify whether to print foreground, background, or both color code tables')
    pt_parser.add_argument('-f', '--foreground', type=int, metavar="[0-255]", choices=range(256), help="specify a foreground color to be on top of the background table")
    pt_parser.add_argument('-b', '--background', type=int, metavar="[0-255]", choices=range(256), help="specify a background color to be the background of the foreground table")
    test_parser = subparsers.add_parser('test', help='test color codes on a string')
    test_parser.add_argument('TEXT', help='text to test')
    test_parser.add_argument('-f', '--foreground', type=int, metavar="[0-255]", choices=range(256), help='specify the foreground color code (0-255)')
    test_parser.add_argument('-b', '--background', type=int, metavar="[0-255]", choices=range(256), help='specify the background color code (0-255)')
    write_parser = subparsers.add_parser('write', help='write a zsh-rc style file that exports all color codes')
    write_parser.add_argument('FILE', type=_pathlib.Path, help='file to write the exports to')
    return parser.parse_args()

def print_table(fg_or_bg, fg, bg):
    color_table = [ [0] * COLS for i in range(ROWS) ]
    color_table.append([0] * (256 % COLS))

    for i in range(256):
        begin = ""
        if fg_or_bg == "fg" and bg and i % 20 == 0:
            begin = COLOR_CODE_FORMAT.format(FGBG=FGBG_TO_CODE["bg"], ID=bg)
        color_table[i // 20][i % 20] = begin + TABLE_FORMAT.format(FGBG=FGBG_TO_CODE[fg_or_bg], ID=i) + (RESET_BG if fg_or_bg == "bg" else RESET_FG) + (RESET_BG if fg_or_bg == "fg" and bg and i % 20 == 19 else "")

    if fg_or_bg == "bg" and fg != -1:
        print(COLOR_CODE_FORMAT.format(FGBG=FGBG_TO_CODE["fg"], ID=fg), end="")
    if fg_or_bg == "fg" and bg != -1:
        print(COLOR_CODE_FORMAT.format(FGBG=FGBG_TO_CODE["bg"], ID=bg), end="")

    print(_tabulate.tabulate(color_table, tablefmt='plain'))

def write_exports(file):
    for i in range(256):
        file.write('export COLOR{}_{}={}\n'.format(i, 'FG', SH_FORMAT.format(FGBG=FGBG_TO_CODE["fg"], ID=i)))
        file.write('export COLOR{}_{}={}\n'.format(i, 'BG', SH_FORMAT.format(FGBG=FGBG_TO_CODE["bg"], ID=i)))
    RESET_FG = 'export COLOR_{}_{}={}\n'.format('RESET', 'FG', "$'%{\e[39m%}'")
    RESET_BG = 'export COLOR_{}_{}={}\n'.format('RESET', 'BG', "$'%{\e[49m%}'")
    file.write(RESET_FG)
    file.write(RESET_BG)

def test_text(text, fg, bg):
    fg_str = ''
    bg_str = ''
    if fg != -1:
        fg_str = TEST_FORMAT.format(FGBG=FGBG_TO_CODE["fg"], CODE=fg)
    if bg != -1:
        bg_str = TEST_FORMAT.format(FGBG=FGBG_TO_CODE["bg"], CODE=bg)

    print(fg_str + bg_str + text + RESET_FG + RESET_BG)

def main():
    args = get_args()

    if 'WHICH' in args:
        fg = -1
        bg = -1
        if 'foreground' in args and args.foreground:
            fg = args.foreground
        if 'background' in args and args.background:
            bg = args.background
        if args.WHICH == 'both':
            print_table('fg', fg, bg)
            print_table('bg', fg, bg)
        else:
            print_table(args.WHICH, fg, bg)
    if 'TEXT' in args and args.TEXT:
        fg = -1
        bg = -1
        if 'foreground' in args and args.foreground:
            fg = args.foreground
        if 'background' in args and args.background:
            bg = args.background
        test_text(args.TEXT, fg, bg)

    if 'FILE' in args and args.FILE:
        if args.FILE.is_file():
            r = input("{} will be overwritten. Are you sure (y/N)? ".format(args.FILE))
            if r.upper() != 'Y':
                exit(1)
        with open(args.FILE, 'w') as f:
            write_exports(f)


