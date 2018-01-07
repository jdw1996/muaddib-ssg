#!/usr/bin/env python3

import os
import sys
import datetime
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
FLAG_CLEAN = "-c"
FLAG_SOURCE_DIR = "-s"
FLAG_BLOG_DIR = "-b"

ARG_DICT = {
    "--help": FLAG_HELP,
    "--clean": FLAG_CLEAN,
    "--source": FLAG_SOURCE_DIR,
    "--blog": FLAG_BLOG_DIR
}

UNIVERSAL_SUBSTITUTIONS = {
    "$YEAR": datetime.datetime.now().year
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

def clean():
    pass

def make_substitutions(file_content, **kwargs):
    """Return a version of file_content with all replacements from kwargs.

    Args:
        file_content (str): The string in which substitutions should be
            made.
        kwargs (dict(str, str)): Keys will be replaced with values.
    """
    content_with_substitutions = file_content
    for key in kwargs:
        content_with_substitutions.replace(key, kwargs[key])
    return content_with_substitutions

# Prepare individual pages and files.

def process_html_page(page_file):
    pass

def process_md_page(page_file):
    pass

def process_md_post(post_file):
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
            new_loa.append(arg)
    return new_loa

def main(**kwargs):
    """Prepare the blog."""
    source_dir = kwargs["source_dir"]
    blog_dir = kwargs["blog_dir"]
    with os.scandir(source_dir) as source_files:
        for entry in source_files:
            entry_name = entry.name
            if entry.is_file():
                extension = os.path.splitext(entry_name)[-1]
                if extension == "html":
                    process_html_page(entry_name)
                elif extension == "md":
                    process_md_page(entry_name)
                elif extension == "css":
                    process_css(entry_name)
                else:
                    raise InvalidFileTypeException(entry.path)
            elif entry_name == blog_dir:
                process_blog(entry)

if __name__ == "__main__":
    source_dir = "_src"
    blog_dir = "blog"
    clean_only = False
    try:
        args = split_flags(sys.argv[1:])
        i = 0
        while i < len(args):
            curr_arg = args[i]
            if curr_arg == FLAG_HELP:
                raise SeekingHelpException
            elif curr_arg == FLAG_CLEAN:
                clean_only = True
                break
            elif curr_arg == FLAG_SOURCE_DIR:
                i += 1
                source_dir = args[i]
            elif curr_arg == FLAG_BLOG_DIR:
                i += 1
                blog_dir = args[i]
            i += 1
        blog_dir = os.path.join(source_dir, blog_dir)
        if not os.path.isdir(source_dir):
            raise InvalidSourceException
        if not os.path.isdir(blog_dir) and not clean_only:
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
        if clean_only:
            clean()
        else:
            main(source_dir=source_dir, blog_dir=blog_dir)
