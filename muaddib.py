#!/usr/bin/env python3

import os
import sys
import datetime
import re

import bs4
from css_html_js_minify import css_minify, html_minify
import markdown as md

# Constants.

SOURCE_DIR = "_src"
BLOG_DIR = os.path.join(SOURCE_DIR, "blog")
PAGE_TEMPLATE = os.path.join(SOURCE_DIR, "_page.html")
POST_TEMPLATE = os.path.join(SOURCE_DIR, "_post.html")
UNIVERSAL_SUBSTITUTIONS = {
    "$YEAR": datetime.datetime.now().year
}

CORRECT_USAGE = (
    "Usage:\n"
    "    muaddib.py"
)
INVALID_ARGUMENTS = "The arguments you entered are invalid."
INVALID_DIR = "The necessary source files do not exist."

FLAG_HELP = "-h"
FLAG_CLEAN = "-c"

ARG_DICT = {
    "--help": FLAG_HELP,
    "--clean": FLAG_CLEAN,
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
                new_loa.append("-" + char)
        elif arg in ARG_DICT.keys():
            new_loa.append(ARG_DICT[arg])
        else:
            new_loa.append(arg)
    return new_loa

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
    for k, v in kwargs.items():
        content_with_substitutions.replace(k, v)
    return content_with_substitutions

# Prepare individual pages and files.

def process_page(page_file, is_markdown):
    """Process page and write to new file for website.

    Args:
        page_file (str): Location of the file to process as a new page.
        is_markdown (bool): If true, page_file is Markdown; else HTML.
    """
    content = ""
    # Read in file contents.
    with open(page_file, "r") as page:
        content = post.read()
    new_filename = page_file
    if is_markdown:
        content = md.markdown(content)
        new_filename = os.path.splitext(new_filename)[0] + ".html"
    # Get title of page.
    title = bs4(content).h1.extract()
    title = title[title.find(">") + 1:]
    title = title[:title.find("<")]
    # Make necessary substitutions.
    substitutions = {}
    substitutions["$BODY"] = content
    substitutions["$TITLE"] = title
    content = \
        make_substitutions(content, **substitutions, **UNIVERSAL_SUBSTITUTIONS)
    content = html_minify(content)
    # Create new file.
    with open(new_filename, "w") as new_file:
        new_file.write(content)

def process_post(post_file, is_markdown):
    """Process post and write to new file for website.

    Args:
        post_file (str): Location of the file to process as a new post.
        is_markdown (bool): If true, post_file is Markdown; else HTML.
    """
    content = ""
    # Read in file contents.
    with open(post_file, "r") as post:
        content = post.read()
    if is_markdown:
        content = md.markdown(content)
    # Get title of post.
    title = bs4(content).h1.extract()
    title = title[title.find(">") + 1:]
    title = title[:title.find("<")]
    # Get date and new filename.
    split_filename = os.path.basename(post_file).split("-")
    year = split_filename[0]
    month = split_filename[1]
    day = split_filename[2]
    date_string = "-".join(split_filename[:3])
    new_filename = "-".join(split_filename[3:])
    if is_markdown:
        new_filename = os.path.splitext(new_filename)[0] + ".html"
    # Make necessary substitutions.
    substitutions = {}
    substitutions["$BODY"] = content
    substitutions["$TITLE"] = title
    substitutions["$DATE"] = date_string
    content = \
        make_substitutions(content, **substitutions, **UNIVERSAL_SUBSTITUTIONS)
    content = html_minify(content)
    # Create new file.
    post_dir = os.path.join(year, month, day)
    os.makedirs(post_dir, exist_ok=True)
    with open(os.path.join(post_dir, new_filename), "w") as new_file:
        new_file.write(content)

def process_css(css_file):
    pass

# Organize the blog.

def process_blog(blog_dir):
    pass

# Compile the site.

def generate():
    """Compile all pages and posts for the website."""
    with os.scandir(SOURCE_DIR) as source_files:
        for entry in source_files:
            entry_name = entry.name
            if entry.is_file():
                extension = os.path.splitext(entry_name)[-1]
                if extension == "html":
                    process_page(entry_name, False)
                elif extension == "md":
                    process_page(entry_name, True)
                elif extension == "css":
                    process_css(entry_name)
                else:
                    continue
            elif entry_name == BLOG_DIR:
                process_blog(entry_name)

def main():
    """Prepare the blog."""
    clean_only = False
    try:
        args = split_flags(sys.argv[1:])
        for arg in args:
            if arg == FLAG_HELP:
                raise SeekingHelpException
            elif arg == FLAG_CLEAN:
                clean_only = True
            else:
                raise InvalidCommandException
        source_valid = os.path.isdir(SOURCE_DIR) and (
            clean_only or (
                os.path.isdir(BLOG_DIR) and
                os.path.isfile(PAGE_TEMPLATE) and
                os.path.isfile(POST_TEMPLATE)
            )
        )
        if not source_valid:
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
            generate()

if __name__ == "__main__":
    main()
