from ascii_graph import Pyasciigraph
from pprint import pprint
from itertools import *
from os.path import basename as _basename
from os.path import normpath
# from os.path import dirname as _basename
import sys, os
from fnmatch import fnmatch



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    GREY ='\033[1;30m'
def colorize(string, color):
    return color + string + bcolors.ENDC

def basename(fpath):
    # print('')
    # print(fpath)
    try:
        last = fpath.split('/')[-2] + '/'
        if last == './': last = ''
    except:
        last = ''

    # print(last)
    plus_last_dir = colorize(last,bcolors.GREY) + _basename(fpath)
    # return plus_last_dir
    return plus_last_dir

def read_sloccount_file(file_):
    with open(file_) as f:
        while 1:
            line = next(f)
            # print(line)
            if line == '\n':
                foo = next(f)
                break
        return list(f)

def main(f, gitignore, locignore):
    print('')
    lines = read_sloccount_file(f)

    try: ignore_items = open(gitignore).read().splitlines()
    except: ignore_items = []
    try: additional_items = open(locignore).read().splitlines()
    except: additional_items = []

    ignore_items += additional_items

    data_raw = (line.split('\t') for line in lines)

    matches_no_ignore_pattern = \
        lambda fname: all(not
                (fnmatch(fname, pattern) or fnmatch(basename(fname), pattern))
                    for pattern in ignore_items)

    filtered_items = []
    for loc, ftype, folder, fname in data_raw:
        loc = int(loc)
        fname = fname.strip()
        if matches_no_ignore_pattern(fname):
            filtered_items.append((loc, ftype, folder, fname))

    number_max_char_places = \
            len(str(max(filtered_items, key=lambda i: len(str(i[0])))[0])) # lol.

    fname_len = lambda fname: len(basename(fname))

    longest_item_by_fname = max(filtered_items,
            key=lambda itemrow: fname_len(itemrow[3]))
    max_fname_char_len = len(basename(longest_item_by_fname[3]))

    format_string = '{:<' + str(max_fname_char_len+2) + '}{}'

    func= lambda line: line[1]
    filtered_items = sorted(filtered_items, key=func)
    loc_by_lang = groupby(filtered_items, key=func)
    graph_content=[]
    for key, group in loc_by_lang:
        print(bcolors.OKBLUE + key.upper() + bcolors.ENDC)
        sum = 0
        for item in group:
            # print(basename(item[3]))
            print(basename(format_string.format(basename(item[3]), str(item[0]).rjust(number_max_char_places))))

            sum += item[0]
        line_len = max_fname_char_len + 2 + number_max_char_places
        sum_formatted = bcolors.HEADER + '\u03a3 ' + str(sum) + bcolors.ENDC
        print(sum_formatted.rjust(line_len-2))
        print('')
        graph_content.append((key, int(sum)))

    graph = Pyasciigraph()
    for line in graph.graph('Summary', graph_content):
        print(line)


if __name__ == '__main__':
    fname = sys.argv[1]
    gitignore = sys.argv[2]
    locignore = sys.argv[3]
    main(fname,gitignore, locignore)

