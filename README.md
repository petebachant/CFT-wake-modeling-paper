# Modeling the near-wake of a vertical-axis cross-flow turbine with 2-D and 3-D RANS

A paper evaluating blade-resolved RANS for modeling CFT wakes. A preprint of the
paper has been posted on [arXiv](http://arxiv.org/abs/1604.02611), and the most
recently built PDF of the paper can be viewed
[here](https://drive.google.com/file/d/0BwMVIAlxIxfZX3ItY3lZcm5zYVE/view?usp=sharing).


## Generating figures

This requires a very specific setup, which is outlined at the top of
`makefigs.py`. Basically, it requires all CFD cases to be solved and located
inside the directories defined. It also requires the experimental repo from
the RVAT-Re-dep experiment--no raw data necessary.

The `makefigs.py` script should be run from an IPython shell thanks to all the
wacky `os.chdir` calls.


## Building

To build the paper:

    make paper

To build the cover letter (not included in the Git repo):

    make cover-letter
