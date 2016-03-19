# Numerical modeling the wake of a vertical-axis cross-flow turbine

A paper evaluating various techniques for modeling CFT wakes.

  * RANS with resolved boundary layers
  * Actuator line with and without free surface
  * More?


## What engineers should learn from this paper

  * How accurate are the various wake modeling techniques? Also, how well
    do these predict performance?
  * What is the lowest-fidelity model that produces acceptable results for
    predicting array performance?


## Generating figures

This requires a very specific setup, which is outlined at the top of
`makefigs.py`. Basically, it requires all CFD cases to be solved and located
inside the directories defined. It also requires the experimental repo from
the RVAT-Re-dep experiment--no raw data necessary.

The `makefigs.py` script should be run from an IPython shell thanks to all the
wacky `os.chdir` calls.


## Building the cover letter

    cd cover-letter
    pandoc --template=template-letter.tex cover-letter.md -o cover-letter.pdf
