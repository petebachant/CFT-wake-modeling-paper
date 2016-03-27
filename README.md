# Modeling the near-wake of a vertical-axis cross-flow turbine with 2-D and 3-D RANS

A paper evaluating blade-resolved RANS for modeling CFT wakes. The most recently
built version of the paper can be viewed
[here](https://drive.google.com/file/d/0BwMVIAlxIxfZX3ItY3lZcm5zYVE/view?usp=sharing).


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
