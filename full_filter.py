#!/usr/bin/env python
""" Filter statsmodels """

import os
from os.path import join as pjoin, splitext, split as psplit
import sys
import re
import shutil
from subprocess import call

TO_RM = \
"""doc
examples
fff2.py
libfffpy
setup_egg.py
setup_fff2.py
tools""".split('\n')

TO_PRESERVE = \
"""lib/statistics
lib/neuroimaging/statistics
lib/neuroimaging/algorithms/statistics
neuroimaging/algorithms/statistics
nipy/algorithms/statistics
neuroimaging/fixes/scipy/stats_models
neuroimaging/fixes/scipy/stats/models
nipy/fixes/scipy/stats/models"""


def strip_trailing(pwd):
    for dirpath, dirnames, filenames in os.walk(pwd):
        if dirpath.endswith('.git'):
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


def rm_list(to_rm):
    for elem in to_rm:
        if os.path.isfile(elem):
            os.unlink(elem)
        elif os.path.isdir(elem):
            shutil.rmtree(elem)


def preserve_list(to_pres):
    pass


def main():
    rm_list(TO_RM)
    preserve_list(TO_PRESERVE)
    strip_trailing(os.getcwd())


if __name__ == '__main__':
    main()
