#!/usr/bin/env python
"""
This script makes the figures for the CFT wake modeling paper.
"""

from __future__ import print_function, division
import matplotlib.pyplot as plt
import os
from pxl.styleplot import set_sns
import pxl.timeseries as ts
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
#sa3dpl = SourceFileLoader("sa3dpl", 
#                  os.path.join(cfd_dirs["3-D"]["SpalartAllmaras"],
#                  "modules", "plotting.py")).load_module()
sst3dpr = SourceFileLoader("sst3dpr", 
                  os.path.join(cfd_dirs["3-D"]["kOmegaSST"],
                  "modules", "processing.py")).load_module()
#exppr = SourceFileLoader("exppl", os.path.join(exp_dir, "Modules", 
#                         "plotting.py")).load_module()
                         
U = 1.0
D = 1.0
nu = 1e-6

def load_exp_data():
    """Loads section of exp wake data for U_infty=1.0 m/s."""
    return pd.read_csv(os.path.join(exp_dir, "Data", "Processed", 
                                    "Wake-1.0.csv"))
                                    
def load_exp_perf_data():
    """Loads section of exp perf data for U_infty=1.0 m/s."""
    return pd.read_csv(os.path.join(exp_dir, "Data", "Processed", 
                                    "Perf-1.0.csv"))

def plot_exp_perf():
    df = load_exp_perf_data()
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(7.5, 3))
    ax[0].plot(df.mean_tsr, df.mean_cp, "-o")
    ax[0].set_ylabel(r"$C_P$")
    ax[1].plot(df.mean_tsr, df.mean_cd, "-o")
    ax[1].set_ylabel(r"$C_D$")
    for a in ax:
        a.set_xlabel(r"$\lambda$")
    fig.tight_layout()
    if save:
        fig.savefig("figures/exp_perf" + savetype)
    
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
        
def plot_profiles():
    """Plot streamwise velocity and TKE profiles for all cases."""
    fig, ax = plt.subplots(1, 2, figsize=(7.5, 3))
    # Load data from 2-D SST case
    os.chdir(cfd_dirs["2-D"]["kOmegaSST"])
    df = sst2dpr.load_u_profile()
    ax[0].plot(df.y_R, df.u, "-", label="SST (2-D)")
    df = sst2dpr.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, "-", label="SST (2-D)")
    # Load data from 2-D SA case
    os.chdir(cfd_dirs["2-D"]["SpalartAllmaras"])
    df = sa2dpr.load_u_profile()
    ax[0].plot(df.y_R, df.u, "-.", label="SA (2-D)")
    df = sa2dpr.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, "-.", label="SA (2-D)")
    # Load data from 3-D SST case
    os.chdir(cfd_dirs["3-D"]["kOmegaSST"])
    df = sst3dpr.load_u_profile()
    ax[0].plot(df.y_R, df.u, "--", label="SST (3-D)")
    df = sa3dpr.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, "--", label="SST (3-D)")
    # Load data from 3-D SA case
    os.chdir(cfd_dirs["3-D"]["SpalartAllmaras"])
    df = sa3dpr.load_u_profile()
    ax[0].plot(df.y_R, df.u, ":", label="SA (3-D)")
    df = sa3dpr.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, ":", label="SA (3-D)")
    # Load data from experiment
    df = load_exp_data()
    df = df[df.z_H == 0]
    ax[0].plot(df.y_R, df.mean_u, "o", label="Exp.", markerfacecolor="none")
    ax[1].plot(df.y_R, df.k, "o", label="Exp.", markerfacecolor="none")
    # Set legend and labels
    ax[1].legend(loc="best")
    for a in ax: a.set_xlabel("$y/R$")
    ax[0].set_ylabel(r"$U/U_\infty$")
    ax[1].set_ylabel(r"$k/U_\infty^2$")
    plt.tight_layout()
    # Move back into this directory
    os.chdir(paper_dir)
    if save:
        fig.savefig("figures/profiles" + savetype)
        
def make_perf_bar_charts():
    """Create bar charts for C_P and C_D for all cases."""
    cp = {}
    cd = {}
    # Load experimental data
    df = load_exp_data()
    cp["Exp."] = df.mean_cp.mean()
    cd["Exp."] = df.mean_cd.mean()
    # Load performance from 2-D SST
    os.chdir(cfd_dirs["2-D"]["kOmegaSST"])
    perf = sst2dpr.calc_perf()
    cp["SST (2-D)"] = perf["C_P"]
    cd["SST (2-D)"] = perf["C_D"]
    # Load performance from 2-D SA
    os.chdir(cfd_dirs["2-D"]["SpalartAllmaras"])
    perf = sa2dpr.calc_perf()
    cp["SA (2-D)"] = perf["C_P"]
    cd["SA (2-D)"] = perf["C_D"]
    # Load performance from 3-D SST
    os.chdir(cfd_dirs["3-D"]["kOmegaSST"])
    perf = sst3dpr.calc_perf()
    cp["SST (3-D)"] = perf["C_P"]
    cd["SST (3-D)"] = perf["C_D"]
    # Load performance from 3-D SA
    os.chdir(cfd_dirs["3-D"]["SpalartAllmaras"])
    perf = sa3dpr.calc_perf()
    cp["SA (3-D)"] = perf["C_P"]
    cd["SA (3-D)"] = perf["C_D"]
    # Make figure
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(7.5, 3))
    names = ["SST (2-D)", "SA (2-D)", "SST (3-D)", "SA (3-D)", "Exp."]
    quantities = [cp[name] for name in names]
    ax[0].bar(range(len(names)), quantities, color="gray", width=0.5,
              edgecolor="black")
    ax[0].set_xticks(np.arange(len(names))+0.25)
    ax[0].set_xticklabels(names, rotation=45)
    ax[0].set_ylabel(r"$C_P$")
    quantities = [cd[name] for name in names]
    ax[1].bar(range(len(names)), quantities, color="gray", width=0.5,
              edgecolor="black")
    ax[1].set_xticks(np.arange(len(names))+0.25)
    ax[1].set_xticklabels(names, rotation=45)
    ax[1].set_ylabel(r"$C_D$")
    fig.tight_layout()
    os.chdir(paper_dir)
    if save:
       fig.savefig("figures/perf_bar_chart" + savetype)
       
def load_exp_recovery():
    """Load recovery terms from experimental data."""
    os.chdir(exp_dir)
    import Modules.plotting as exppl
    wm = exppl.WakeMap(1.0)
    dUdy = wm.dUdy
    dUdz = wm.dUdz
    tt = wm.ddy_upvp + wm.ddz_upwp
    d2Udy2 = wm.d2Udy2
    d2Udz2 = wm.d2Udz2
    meanu, meanv, meanw = wm.df.mean_u, wm.df.mean_v, wm.df.mean_w
    y_R, z_H = wm.y_R, wm.z_H
    return {"y_adv": ts.average_over_area(-meanv*dUdy/meanu/U*D, y_R, z_H),
            "z_adv": ts.average_over_area(-meanw*dUdz/meanu/U*D, y_R, z_H),
            "turb_trans": ts.average_over_area(-tt/meanu/U*D, y_R, z_H),
            "visc_trans": ts.average_over_area(nu*(d2Udy2 + d2Udz2)/meanu/U*D, 
                                               y_R, z_H),
            "pressure_trans": np.nan}
       
def make_recovery_bar_chart():
    """
    Create a bar chart with x-labels for each recovery term and 5 different
    bars per term, corresponding to each CFD case and the experimental data.
    """
    data = {}
    # Load recovery terms from 2-D SST case
    os.chdir(cfd_dirs["2-D"]["kOmegaSST"])
    data["SST (2-D)"] = sa2dpr.read_funky_log()
    # Load recovery terms from 2-D SA case
    os.chdir(cfd_dirs["2-D"]["SpalartAllmaras"])
    data["SA (2-D)"] = sst2dpr.read_funky_log()
    # Load recovery terms from 3-D SST case (0.0 for now)
    os.chdir(cfd_dirs["3-D"]["kOmegaSST"])
    data["SST (3-D)"] = sst3dpr.read_funky_log()
    # Load recovery terms from 3-D SA case
    os.chdir(cfd_dirs["3-D"]["SpalartAllmaras"])
    data["SA (3-D)"] = sa3dpr.read_funky_log()
    
    # Load experimental data
    data["Exp."] = load_exp_recovery()

    # Create figure
    names = [r"$-V \frac{\partial U}{\partial y}$", 
             r"$-W \frac{\partial U}{\partial z}$", 
             r"Turb. trans.",
             r"$-\frac{\partial P}{\partial x}$",
             r"Visc. trans."]
    quantities = ["y_adv", "z_adv", "turb_trans", "pressure_trans",
                  "visc_trans"]
    cases = ["SST (2-D)", "SA (2-D)", "SST (3-D)", "SA (3-D)", "Exp."]
    areas = [3.66*1.0, 3.66*1.0, 3.66*2.44, 3.66*2.44, 3.0*0.625]
    fig, ax = plt.subplots(figsize=(7.5, 3.5))
    cm = plt.cm.coolwarm
    
    # Plot all recovery terms
    for n, case in enumerate(cases):
        q = [data[case][v] for v in quantities]
        q = np.array(q)*areas[n]
        color = cm(int(n/4*256))
        ax.bar(np.arange(len(names)) + n*.15, q, color=color, width=0.15, 
               edgecolor="black", label=case)
    ax.set_xticks(np.arange(len(names)) + 5*.15/2)
    ax.set_xticklabels(names)
    ax.hlines(0, 0, len(names), color="gray")
    ax.set_ylabel(r"$\frac{U \, \mathrm{ transport} \times A_c}"
                  "{UU_\infty D^{-1}}$")
    ax.legend(loc="best", ncol=1)
    fig.tight_layout()

    
    os.chdir(paper_dir)
    if save:
        fig.savefig("figures/mom_bar_graph"+savetype)
    
    for k,v in data.items():
        print(k)
        print(v)
    
    
if __name__ == "__main__":
    if not os.path.isdir("figures"):
        os.mkdir("figures")
    set_sns()
    plt.rcParams["axes.grid"] = True
    
    save = True
    savetype = ".pdf"
    
    plot_exp_perf()
#    plot_exp_meancontquiv()
#    plot_cfd_meancontquiv("kOmegaSST")
#    plot_cfd_meancontquiv("SpalartAllmaras")
#    plot_cfd_u_profile()
#    plot_verification()
#    plot_profiles()
#    make_perf_bar_charts()
#    make_recovery_bar_chart()
    plt.show()
