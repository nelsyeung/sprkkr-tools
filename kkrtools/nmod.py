#!/usr/bin/env python3
"""Miscellaneous useful functions."""


def replace_text(text, reps):
    """Replace all the matching strings from a piece of text."""
    for i, j in reps.items():
        text = text.replace(str(i), str(j))

    return text


def find_first_line(filepath, string):
    """Return first encountered line from a file with the matching string."""
    value = ''

    with open(filepath, 'r') as f:
        for line in f:
            if string in line:
                value = line
                break

    return value.rstrip()


def modify_file(original, new, reps):
    """Modify the specified file with replacements to a new location."""
    with open(new, 'w+') as fnew:
        with open(original, 'r') as foriginal:
            for line in foriginal:
                fnew.write(replace_text(line, reps))
