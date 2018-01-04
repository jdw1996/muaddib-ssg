#!/usr/bin/env python3

import os
import sys
import re

import bs4
from css_html_js_minify import css_minify, html_minify
import markdown as md

# Constants.

CORRECT_USAGE = (
    "Usage:\n"
    "    muaddib.py"
)
INVALID_ARGUMENTS = "The arguments you entered are invalid."
INVALID_SOURCE_DIR = "The source directory you indicated does not exist."

FLAG_HELP = "-h"
FLAG_SOURCE = "-s"

ARG_DICT = {
    "--help": FLAG_HELP,
    "--source": FLAG_SOURCE
}

# Utilities.

class InvalidCommandException(Exception):
    pass

class SeekingHelpException(Exception):
    pass

class InvalidSourceException(Exception):
    pass

# Prepare individual pages.

# Organize pages into site.

# Compile the site.

def split_flags(loa):
    """Return a version of loa with single letter flags split apart.

    Args:
        loa (List(str)): The list of arguments in which the flags must be
            split.
    """
    new_loa = []
    for arg in loa:
        if re.fullmatch("-[a-zA-Z]+", arg):
            for char in arg[1:]:
                flag = "-" + char
                if flag not in ARG_DICT.values():
                    raise InvalidCommandException
                new_loa.append("-" + char)
        elif arg in ARG_DICT.keys():
            new_loa.append(ARG_DICT[arg])
        else:
            raise InvalidCommandException
    return new_loa

def main(**kwargs):
    pass

if __name__ == "__main__":
    source_dir = "_src"
    try:
        args = split_flags(sys.argv[1:])
        i = 0
        while i < len(args):
            curr_arg = args[i]
            if curr_arg == FLAG_HELP:
                break
            elif curr_arg == FLAG_SOURCE:
                i += 1
                source_dir = curr_arg
            i += 1
        if not os.path.isdir(source_dir):
            raise InvalidSourceException
    except InvalidCommandException:
        print(INVALID_ARGUMENTS)
        print(CORRECT_USAGE)
    except SeekingHelpException:
        print(CORRECT_USAGE)
    except InvalidSourceException:
        print(INVALID_SOURCE_DIR)
        print(CORRECT_USAGE)
    else:
        main(source_dir=source_dir)
