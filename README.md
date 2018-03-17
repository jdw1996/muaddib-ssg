# Muad'Dib Static Site Generator

> **Paul:**  How do you call among you the little mouse, the mouse that jumps?
>
> **Stilgar:**  We call that one *muad'dib*.
>
> &mdash; <cite>*Dune*, by Frank Herbert</cite>

I've been using Jekyll for my personal website up until this point, but decided
to create my own static site generator.  I didn't have any specific problems
with Jekyll, but I wanted to have more control and thought it might be fun to
build do.

The Muad'Dib SSG is intended to be simple and lightweight, and do precisely
what's necessary for my website.  All features are subject to change and I
won't be adding any features I'm not using.

You can see my website [here](https://jdw1996.github.io/).  It is the only site
I am aware of that uses Muad'Dib.  I also wrote a post providing some
background on this project, available
[here](https://jdw1996.github.io/2018-03-12-writing-my-own-static-site-generator-with-a-makefile.html).

## Usage

Muad'Dib expects a subdirectory `_src` containing the following files:
* `_post.html`: Template for blog posts.
* `index.md`: Content of the main page.  The first line should be an HTML
  comment containing the website title.
* `_index.html`: Template for the main page.
* `_style.css`: Stylesheet for the website.
* `*.md`: Any number of these files, which contain blog posts.  The first line
  should be an HTML comment containing the post title and the second should be
  an HTML comment containing the post date.

The `_post.html` and `_index.html` files can contain any of the following
variables:
* `{{TITLE}}`: The title of the page/post, taken from the corresponding
  Markdown file.
* `{{YEAR}}`: The current year; this is useful for copyright notices.
* `{{BODY}}`: The content of the corresponding Markdown file, converted to
  HTML.  This should appear on a line on its own.

Additionally, `_post.html` can contain the variable:
* `{{DATE}}`: The date of the post, taken from the corresponding Markdown file.

To generate the website, run `muaddib`.  To delete all files that can be
regenerated from source, run `muaddib clean`.
