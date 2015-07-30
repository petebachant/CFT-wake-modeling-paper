#!/usr/bin/env python
"""
This script makes the figures for the CFT wake modeling paper.
"""

from __future__ import print_function, division
import matplotlib.pyplot as plt
import os
from pxl.styleplot import set_sns
import pandas as pd
import numpy as np
from importlib.machinery import SourceFileLoader

cfd_sst_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-3d/mesh14"
cfd_sa_dir = "/media/pete/Data2/OpenFOAM/pete-2.3.x/run/unh-rvat-3d/mesh14-sa"
cfd_sst_2d_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-2d/kOmegaSST"
cfd_sa_2d_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-2d/SpalartAllmaras"
exp_dir = "/home/pete/Google Drive/Research/Experiments/RVAT Re dep"
paper_dir = "/home/pete/Google Drive/Research/Papers/CFT wake modeling"
cfd_dirs = {"3-D": {"kOmegaSST": cfd_sst_dir, 
                    "SpalartAllmaras": cfd_sa_dir},
            "2-D": {"kOmegaSST": cfd_sst_2d_dir, 
                    "SpalartAllmaras": cfd_sa_2d_dir}}

# Import individual modules from each case
sst2dpr = SourceFileLoader("sst2dpr", 
                  os.path.join(cfd_dirs["2-D"]["kOmegaSST"],
                  "modules", "processing.py")).load_module()
sa2dpr = SourceFileLoader("sa2dpr", 
                  os.path.join(cfd_dirs["2-D"]["SpalartAllmaras"],
                  "modules", "processing.py")).load_module()
sa3dpr = SourceFileLoader("sa3dpr", 
                  os.path.join(cfd_dirs["3-D"]["SpalartAllmaras"],
                  "modules", "processing.py")).load_module()
sa3dpl = SourceFileLoader("sa3dpl", 
                  os.path.join(cfd_dirs["3-D"]["SpalartAllmaras"],
                  "modules", "plotting.py")).load_module()

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
    os.chdir(cfd_dirs["3-D"][case])
    if case == "SpalartAllmaras":
        sa3dpl.plot_meancontquiv()
    elif case == "kOmegaSST":
        sst3dpl.plot_meancontquiv()
    os.chdir(paper_dir)
    if save:
         plt.savefig("figures/meancontquiv_" + case + savetype)
         
def plot_cfd_u_profile(case="kOmegaSST", dims="2-D"):
    """Plot mean streamwise velocity profile."""
    os.chdir(cfd_dirs[dims][case])
    import modules.plotting as plotting_cfd
    plotting_cfd.plot_u()
    os.chdir(paper_dir)
    
def deltat_to_steps_per_rev(deltat):
    """Convert deltaT to stepsPerRev."""
    tsr = 1.9
    U_infty = 1.0
    R = 0.5
    omega = tsr*U_infty/R
    rev_per_sec = omega/(2*np.pi)
    sec_per_step = deltat
    step_per_rev = sec_per_step**(-1)*rev_per_sec**(-1)
    return step_per_rev
    
def plot_verification():
    """Create verification figure."""
    p = os.path.join(cfd_dirs["2-D"]["SpalartAllmaras"], "processed", 
                     "timestep_dep.csv")
    df_ts_sa = pd.read_csv(p)
    df_nx_sa = pd.read_csv(p.replace("timestep_dep", "spatial_grid_dep"))
    df_nx_sa.sort("nx", inplace=True)
    p = os.path.join(cfd_dirs["2-D"]["kOmegaSST"], "processed", 
                     "timestep_dep.csv")
    df_ts_sst = pd.read_csv(p)
    df_nx_sst = pd.read_csv(p.replace("timestep_dep", "spatial_grid_dep"))
    # Convert deltaT to stepsPerRev
    df_ts_sa["steps_per_rev"] = deltat_to_steps_per_rev(df_ts_sa.dt)
    df_ts_sst["steps_per_rev"] = deltat_to_steps_per_rev(df_ts_sst.dt)
    # Create subplots to use for time (left) and space (right)
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(7.5, 3.25))
    # Create steps per rev plot
    ax[0].plot(df_ts_sst["steps_per_rev"], df_ts_sst["cp"], "-o", label="SST")
    ax[0].plot(df_ts_sa["steps_per_rev"], df_ts_sa["cp"], "-^", label="SA")
    ax[0].set_xlabel(r"Time steps per rev.")
    ax[0].set_ylabel(r"$C_P$")
    # Annotate the chosen time steps
    arrowprops = {"facecolor": "black", "linewidth": 0, "width": 2,
                  "alpha": 0.5}
    ax[0].annotate(r"$\Delta t = 0.002$", xy=(850, 0.514), xytext=(1000, 0.6),
                   arrowprops=arrowprops)
    ax[0].annotate(r"$\Delta t = 0.001$", xy=(1655, 0.49), xytext=(1800, 0.65),
                   arrowprops=arrowprops)
    ax[0].grid(True)
    # Create nx plot
    ax[1].plot(df_nx_sst["nx"], df_nx_sst["cp"], "-o", label="SST")
    ax[1].plot(df_nx_sa["nx"], df_nx_sa["cp"], "-^", label="SA")
    ax[1].set_xlabel(r"$N_x$")
    ax[1].legend(loc="lower right")
    ax[1].grid(True)
    fig.tight_layout()
    if save:
        fig.savefig("figures/verification" + savetype)
        
def plot_u_profiles():
    """Plot streamwise velocity profiles for all cases."""
    fig, ax = plt.subplots()
    # Load data from 2-D SST case
    os.chdir(cfd_dirs["2-D"]["kOmegaSST"])
    df = sst2dpr.load_u_profile()
    ax.plot(df.y_R, df.u, "-", label="SST (2-D)")
    # Load data from 2-D SA case
    os.chdir(cfd_dirs["2-D"]["SpalartAllmaras"])
    df = sa2dpr.load_u_profile()
    ax.plot(df.y_R, df.u, "--", label="SA (2-D)")
    # Load data from 3-D SA case
    os.chdir(cfd_dirs["3-D"]["SpalartAllmaras"])
    df = sa3dpr.load_u_profile()
    ax.plot(df.y_R, df.u, "-.", label="SA (3-D)")
    ax.legend(loc="best")
    ax.set_xlabel("$y/R$")
    ax.set_ylabel(r"$U/U_\infty$")
    plt.tight_layout()
    # Move back into this directory
    os.chdir(paper_dir)
    
if __name__ == "__main__":
    if not os.path.isdir("figures"):
        os.mkdir("figures")
    set_sns()
    plt.rcParams["axes.grid"] = True
    
#    plot_exp_perf_curve()
#    plot_exp_meancontquiv()
#    plot_cfd_meancontquiv("kOmegaSST")
#    plot_cfd_meancontquiv("SpalartAllmaras")
#    plot_cfd_u_profile()
#    plot_verification()
    plot_u_profiles()
    plt.show()
