#!/usr/bin/python3

"""
Markdown to HTML conversion script.
"""

import sys
import os.path
import re
import hashlib


def usage_error():
    """
    Prints usage error message.
    """
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)


def file_missing_error(filename):
    """
    Prints file missing error message.
    """
    print("Missing {}".format(filename), file=sys.stderr)


def remove_c(content):
    """
    Removes all occurrences of 'c' or 'C' from content.
    """
    return content.replace('c', '').replace('C', '')


def convert_md5(content):
    """
    Converts content to MD5 hash.
    """
    return hashlib.md5(content.encode()).hexdigest()


def convert_markdown_to_html(markdown_file, html_file):
    """
    Converts Markdown file to HTML.
    """
    if not os.path.isfile(markdown_file):
        file_missing_error(markdown_file)
        return

    with open(markdown_file, 'r') as md_file, open(html_file, 'w') as html_file:
        unordered_list = False
        ordered_list = False
        paragraph = False

        for line in md_file:
            # Headings
            match = re.match(r'^(#+)\s(.*)', line)
            if match:
                heading_level = len(match.group(1))
                html_file.write(f"<h{heading_level}>{match.group(2)}</h{heading_level}>\n")
                continue

            # Unordered list
            if line.startswith('-'):
                if not unordered_list:
                    html_file.write("<ul>\n")
                    unordered_list = True
                html_file.write(f"<li>{line.strip('-').strip()}</li>\n")
                continue
            elif unordered_list:
                html_file.write("</ul>\n")
                unordered_list = False

            # Ordered list
            if line.startswith('*'):
                if not ordered_list:
                    html_file.write("<ol>\n")
                    ordered_list = True
                html_file.write(f"<li>{line.strip('*').strip()}</li>\n")
                continue
            elif ordered_list:
                html_file.write("</ol>\n")
                ordered_list = False

            # Paragraph
            if line.strip():
                if not paragraph:
                    html_file.write("<p>\n")
                    paragraph = True
                html_file.write(f"{line.strip()}\n")
            elif paragraph:
                html_file.write("</p>\n")
                paragraph = False

        # Close any open tags
        if unordered_list:
            html_file.write("</ul>\n")
        if ordered_list:
            html_file.write("</ol>\n")
        if paragraph:
            html_file.write("</p>\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage_error()
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    convert_markdown_to_html(markdown_file, html_file)
