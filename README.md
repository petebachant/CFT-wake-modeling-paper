# Modeling the near-wake of a vertical-axis cross-flow turbine with 2-D and 3-D RANS

Source files for our paper evaluating blade-resolved RANS for modeling CFT wakes.

Relevant links:

* [Preprint on arXiv](http://arxiv.org/abs/1604.02611)
* [Most recently built PDF](https://drive.google.com/file/d/0BwMVIAlxIxfZX3ItY3lZcm5zYVE/view?usp=sharing)
* [Version published in the Journal of Renewable and Sustainable Energy](http://dx.doi.org/10.1063/1.4966161)


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
