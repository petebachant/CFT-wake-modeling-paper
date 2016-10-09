#!/usr/bin/env bash
# This script creates a diff version comparing the recent with whatever revision
# is supplied as the first argument. This can be any valid Git identifier, e.g.,
# a commit hash, tag, etc.

CURRENT=$(git describe --always --dirty)
rev=$1
if [ "$rev" = "" ]; then
    rev=$(git tag | tail -n1)
fi
git show $rev:paper.tex > archive/paper-$rev-$CURRENT.tex
latexdiff --exclude-textcmd="section,subsection,subsubsection" --math-markup=off archive/paper-$rev-$CURRENT.tex paper.tex > paper-$rev-$CURRENT-diff.tex
latexmk paper-$rev-$CURRENT-diff.tex -pdf -f
mv paper-$rev-$CURRENT-diff.pdf archive
rm paper-$rev-$CURRENT*
