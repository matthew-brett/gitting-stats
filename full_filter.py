#!/usr/bin/env python
""" Filter statsmodels """

import os
from os.path import join as pjoin, splitext
import sys
import re
import shutil
from subprocess import call

def strip_trailing(pwd):
    for dirpath, dirnames, filenames in os.walk(pwd):
        if dirpath == '.git':
            dirnames = []
            continue
        for fname in filenames:
            base, ext = splitext(fname)
            if not ext in ('.py', '.pyx'):
                continue
            newlines = []
            fullfile = pjoin(dirpath, fname)
            for line in open(fullfile, 'rt'):
                newlines.append(line.rstrip() + '\n')
            os.unlink(fullfile)
            fileobj = open(fullfile, 'w')
            fileobj.writelines(newlines)
            fileobj.close()


def main():
    # An example command
    try:
        shutil.rmtree('nipy/algorithms')
    except OSError:
        pass
    strip_trailing(os.getcwd())


if __name__ == '__main__':
    main()
