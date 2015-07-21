#!/usr/bin/env python
"""
This script makes the figures for the CFT wake modeling paper.
"""

from __future__ import print_function, division
import matplotlib.pyplot as plt
import os

cfd_sst_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-3d/mesh14"
cfd_sa_dir = "/media/pete/Data2/OpenFOAM/pete-2.3.x/run/unh-rvat-3d/mesh14-sa"
cfd_sst_2d_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-2d/kOmegaSST"
cfd_sa_2d_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-2d/SpalartAllmaras"
cfd_alm_dir = ""
exp_dir = "/home/pete/Google Drive/Research/Experiments/RVAT Re dep"
paper_dir = os.getcwd()
cfd_dirs = {"kOmegaSST": cfd_sst_dir, "SpalartAllmaras": cfd_sa_dir}
cfd_dirs_2d = {"kOmegaSST": cfd_sst_2d_dir, "SpalartAllmaras": cfd_sa_2d_dir}

save = True
savetype = ".pdf"

def plot_exp_perf_curve():
    os.chdir(exp_dir)
    import Modules.plotting as plotting_exp
    plotting_exp.plot_cp_curve(1.0, show=False)
    os.chdir(paper_dir)
    if save:
        plt.savefig("figures/perf_curve_exp" + savetype)
    
def plot_exp_meancontquiv():
    os.chdir(exp_dir)
    import Modules.plotting as plotting_exp
    plotting_exp.plot_meancontquiv(1.0)
    os.chdir(paper_dir)
    if save:
        plt.savefig("figures/meancontquiv_exp" + savetype)

def plot_cfd_meancontquiv(case="kOmegaSST"):
    """Plots wake mean velocity contours/quivers from 3-D CFD case."""
    os.chdir(cfd_dirs[case])
    import processing as processing_cfd
    processing_cfd.plot_meancontquiv()
    os.chdir(paper_dir)
    if save:
         plt.savefig("figures/meancontquiv_" + case + savetype)
    
def main():
    plot_exp_perf_curve()
    plot_exp_meancontquiv()
    plot_cfd_meancontquiv("kOmegaSST")
    plot_cfd_meancontquiv("SpalartAllmaras")
    plt.show()
    
if __name__ == "__main__":
    if not os.path.isdir("figures"):
        os.mkdir("figures")
    main()