#################################
Making a git repo for statsmodels
#################################

Setting up::

    cd # HOME
    mkdir gitstat
    cd gitstat
    bzr branch lp:statsmodels
    easy_install -U bzr # gives me 2.3.0
    bzr branch lp:python-fastimport # revno 301
    cd python-fastimport
    python setup.py develop # Make you you have this one on the path too
    # Otherwise you may hit a unicode decode error when importing
    cd ..
    bzr branch lp:bzr-fastimport # revno 305
    mkdir ~/.bazaar/plugins
    ln -s ~/gitstat/bzr-fastimport ~/.bazaar/plugins/fastimport
    git clone git://github.com/matthew-brett/git-bzr.git
    # Assuming ~/bin is on your path
    ln -s ~/gitstat/git-bzr/git-bzr ~/bin/git-bzr
    git clone git://github.com/matthew-brett/gitting-stats.git

OK.  Ready to make the first import::

    mkdir draft-statsmodels
    cd draft-statsmodels
    git init
    git bzr add bzr-statsmodels ../statsmodels
    git bzr fetch bzr-statsmodels
    git co -b master bzr/bzr-statsmodels

OK.  That took a few minutes.  Let's make another copy for safety::

    cd ..
    git clone --no-hardlinks draft-statsmodels working-statsmodels
    cd working-statsmodels
    git config core.autocrlf true

Checks::

    $ diff -r . ../statsmodels

    Only in ../statsmodels: .bzr
    Only in .: .git
    Only in .: nipy

There's a stray file in ``nipy/algorithms`` for some reason.  We need to filter
that out.

*********
Filtering
*********

Try::

    git filter-branch --tree-filter /path/to/gitting-stats/full_filter.py --prune-empty

This just to show it can be done.  It will be slow.

**********
Some notes
**********

To show all the authors with their commit ids::

      git log | grep '^Author' | cut -d' ' -f 2- | sort | uniq


Repo statistics collected by application of commands like::

    git co master
    git log --name-only --follow --all -- nipy/fixes/scipy/stats/models/__init__.py

then checking out the commit where the trail goes cold to see where the files
went::

    lib/statistics
    lib/neuroimaging/statistics
    lib/neuroimaging/algorithms/statistics
    neuroimaging/algorithms/statistics
    nipy/algorithms/statistics

    neuroimaging/fixes/scipy/stats_models
    neuroimaging/fixes/scipy/stats/models
    nipy/fixes/scipy/stats/models

When moving away from nipy, Skipper first moved everything to a ``models`` top
level directory, and thence to ``scikits``.  We can probably safely delete
top-level nipy stuff like::

    doc
    examples
    fff2.py
    libfffpy
    setup_egg.py
    setup_fff2.py
    tools
