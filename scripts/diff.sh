#!/usr/bin/env bash
# This script creates a diff version comparing the recent with whatever revision
# is supplied as the first argument. This can be any valid Git identifier, e.g.,
# a commit hash, tag, etc.

CURRENT=$(git describe --always --dirty)
rev=$1
git show $rev:paper.tex > archive/paper-$CURRENT-$rev.tex
latexdiff --exclude-textcmd="section,subsection,subsubsection" --math-markup=off archive/paper-$CURRENT-$rev.tex paper.tex > paper-$CURRENT-$rev-diff.tex
latexmk paper-$CURRENT-$rev-diff.tex -pdf -f
mv paper-$CURRENT-$rev-diff.pdf archive
rm paper-$CURRENT-$rev*
