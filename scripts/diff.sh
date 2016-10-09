#!/usr/bin/env bash
# This script creates a diff version comparing the current version with the
# most recent tagged version

PREVIOUS=$(git tag | tail -n1)
CURRENT=$(git describe --always --dirty)

# If current version is a tag, use one tag prior
if [ $CURRENT = $PREVIOUS ]
then
    PREVIOUS=$(git tag | tail -n2 | head -n1)
fi

git show $PREVIOUS:paper.tex > archive/paper-$PREVIOUS.tex
latexdiff --exclude-textcmd="section,subsection,subsubsection" --math-markup=off archive/paper-$PREVIOUS.tex paper.tex > paper-$PREVIOUS-$CURRENT-diff.tex
latexmk paper-$PREVIOUS-$CURRENT-diff.tex -pdf -f
mv paper-$PREVIOUS-$CURRENT-diff.pdf archive
rm paper-$PREVIOUS-$CURRENT*
