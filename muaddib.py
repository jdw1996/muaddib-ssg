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
INVALID_DIR = "The source directories you indicated do not exist."

FLAG_HELP = "-h"
FLAG_SOURCE_DIR = "-s"
FLAG_BLOG_DIR = "-b"

ARG_DICT = {
    "--help": FLAG_HELP,
    "--source": FLAG_SOURCE_DIR,
    "--blog": FLAG_BLOG_DIR
}

# Utilities.

class InvalidCommandException(Exception):
    pass

class SeekingHelpException(Exception):
    pass

class InvalidSourceException(Exception):
    pass

class InvalidFileTypeException(Exception):
    pass

# Prepare individual pages and files.

def process_html_page(page_file):
    pass

def process_md_page(page_file):
    pass

def process_css(css_file):
    pass

# Organize the blog.

def process_blog(blog_dir):
    pass

# Compile the site.

def split_flags(loa):
    """Return a version of loa with single letter flags split apart.

    Args:
        loa (list(str)): The list of arguments in which the flags must be
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
    """Prepare the blog."""
    source_dir = kwargs["source_dir"]
    blog_dir = kwargs["blog_dir"]
    with os.scandir(source_dir) as source_files:
        for entry in source_files:
            if entry.is_file():
                extension = os.path.splitext(entry.name)[-1]
                if extension == "html":
                    process_html_page(entry)
                elif extension == "md":
                    process_md_page(entry)
                elif extension == "css":
                    process_css(entry)
                else:
                    raise InvalidFileTypeException(entry.path)
            elif entry.name == blog_dir:
                process_blog(entry)

if __name__ == "__main__":
    source_dir = "_src"
    blog_dir = "blog"
    try:
        args = split_flags(sys.argv[1:])
        i = 0
        while i < len(args):
            curr_arg = args[i]
            if curr_arg == FLAG_HELP:
                break
            elif curr_arg == FLAG_SOURCE_DIR:
                i += 1
                source_dir = curr_arg
            elif curr_arg == FLAG_BLOG_DIR:
                i += 1
                blog_dir = curr_arg
            i += 1
        if not os.path.isdir(source_dir):
            raise InvalidSourceException
        if not os.path.isdir(os.path.join(source_dir, blog_dir)):
            raise InvalidSourceException
    except InvalidCommandException:
        print(INVALID_ARGUMENTS)
        print(CORRECT_USAGE)
    except SeekingHelpException:
        print(CORRECT_USAGE)
    except InvalidSourceException:
        print(INVALID_DIR)
        print(CORRECT_USAGE)
    else:
        main(source_dir=source_dir, blog_dir=blog_dir)
