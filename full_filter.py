#!/usr/bin/env python
""" Filter statsmodels """

import os
from os.path import join as pjoin, splitext, split as psplit
import sys
import re
import shutil
from subprocess import call

TO_RM = \
"""nipy
neuroimaging
lib
doc
examples
fff2.py
libfffpy
setup_egg.py
setup_fff2.py
tools""".split('\n')

TO_PRESERVE = [
    ('stats', ('lib/statistics',
              'lib/neuroimaging/statistics',
              'lib/neuroimaging/algorithms/statistics',
              'neuroimaging/algorithms/statistics',
              'nipy/algorithms/statistics')),
    ('scipy_models', ('neuroimaging/fixes/scipy/stats_models',
                     'neuroimaging/fixes/scipy/stats/models',
                     'nipy/fixes/scipy/stats/models'))
]


def strip_trailing(pwd):
    for dirpath, dirnames, filenames in os.walk(pwd):
        if dirpath.endswith('.git'):
            dirnames = []
            continue
        for fname in filenames:
            base, ext = splitext(fname)
            if not ext in ('.py', '.pyx', '.txt', '.rst', '.c'):
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
    preserves = []
    for outdir, sources in to_pres:
        for source in sources:
            if os.path.isdir(source):
                preserves.append((outdir, source))
                os.rename(source, outdir)
                break
    return preserves


def restore_list(to_restore):
    for outdir, source in to_restore:
        assert os.path.isdir(outdir)
        root, sdir = psplit(source)
        os.makedirs(root)
        os.rename(outdir, source)


def main():
    preserves = preserve_list(TO_PRESERVE)
    rm_list(TO_RM)
    restore_list(preserves)
    strip_trailing(os.getcwd())


if __name__ == '__main__':
    main()
