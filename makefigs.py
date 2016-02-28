#!/usr/bin/env python
"""This script makes the figures for the CFT wake modeling paper."""

from __future__ import print_function, division
import matplotlib.pyplot as plt
import os
from pxl.styleplot import set_sns
import pxl.timeseries as ts
import pandas as pd
import numpy as np
import sys

cfd_sst_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-3d/mesh14"
cfd_sa_dir = "/media/Data2/OpenFOAM/pete-2.3.x/run/unh-rvat-3d/mesh14-sa"
cfd_sst_2d_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-2d/kOmegaSST"
cfd_sa_2d_dir = "/media/pete/Data1/OpenFOAM/pete-2.3.x/run/unh-rvat-2d/SpalartAllmaras"
exp_dir = "/home/pete/Google Drive/Research/Experiments/RVAT Re dep"
paper_dir = "/home/pete/Google Drive/Research/Papers/CFT wake modeling"
cfd_dirs = {"3-D": {"kOmegaSST": cfd_sst_dir,
                    "SpalartAllmaras": cfd_sa_dir},
            "2-D": {"kOmegaSST": cfd_sst_2d_dir,
                    "SpalartAllmaras": cfd_sa_2d_dir}}

# Append directories to path so we can import their respective packages
for d in [cfd_sst_dir, cfd_sa_dir, cfd_sst_2d_dir, cfd_sa_2d_dir, exp_dir]:
    if not d in sys.path:
        sys.path.append(d)

import pyurof3dsst, pyurof3dsa, pyurof2dsst, pyurof2dsa, pyrvatrd
import pyrvatrd.plotting

cfd_packages = {"3-D": {"kOmegaSST": pyurof3dsst,
                        "SpalartAllmaras": pyurof3dsa},
                "2-D": {"kOmegaSST": pyurof2dsst,
                        "SpalartAllmaras": pyurof2dsa}}

U = 1.0
D = 1.0
nu = 1e-6
savetype = ".pdf"


def load_exp_data():
    """Loads section of exp wake data for U_infty=1.0 m/s."""
    return pd.read_csv(os.path.join(exp_dir, "Data", "Processed",
                                    "Wake-1.0.csv"))


def load_exp_perf_data():
    """Loads section of exp perf data for U_infty=1.0 m/s."""
    return pd.read_csv(os.path.join(exp_dir, "Data", "Processed",
                                    "Perf-1.0.csv"))


def plot_exp_perf(save=False):
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


def plot_exp_meancontquiv(save=False):
    os.chdir(exp_dir)
    pyrvatrd.plotting.plot_meancontquiv(1.0)
    os.chdir(paper_dir)
    if save:
        plt.savefig("figures/meancontquiv_exp" + savetype)


def plot_exp_kcont(save=False):
    os.chdir(exp_dir)
    wm = pyrvatrd.plotting.WakeMap(1.0)
    wm.plot_k()
    os.chdir(paper_dir)
    if save:
        plt.savefig("figures/kcont_exp" + savetype)


def plot_cfd_meancontquiv(case="kOmegaSST", save=False):
    """Plots wake mean velocity contours/quivers from 3-D CFD case."""
    os.chdir(cfd_dirs["3-D"][case])
    cfd_packages["3-D"][case].plotting.plot_meancontquiv()
    os.chdir(paper_dir)
    if save:
         plt.savefig("figures/meancontquiv_" + case + savetype)


def plot_cfd_kcont(case="kOmegaSST", save=False):
    """Plot TKE from 3-D CFD case."""
    os.chdir(cfd_dirs["3-D"][case])
    cfd_packages["3-D"][case].plotting.plot_kcont()
    os.chdir(paper_dir)
    if save:
         plt.savefig("figures/kcont_" + case + savetype)


def plot_cfd_u_profile(case="kOmegaSST", dims="2-D"):
    """Plot mean streamwise velocity profile."""
    os.chdir(cfd_dirs[dims][case])
    cfd_packages[dims][case].plotting.plot_u()
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


def plot_verification(save=False):
    """Create verification figure."""
    p = os.path.join(cfd_dirs["2-D"]["SpalartAllmaras"], "processed",
                     "timestep_dep.csv")
    df_ts_sa = pd.read_csv(p)
    df_nx_sa = pd.read_csv(p.replace("timestep_dep", "spatial_grid_dep"))
    df_nx_sa.sort_values(by="nx", inplace=True)
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


def plot_profiles(save=False):
    """Plot streamwise velocity and TKE profiles for all cases."""
    fig, ax = plt.subplots(1, 2, figsize=(7.5, 3))
    # Load data from 2-D SST case
    os.chdir(cfd_dirs["2-D"]["kOmegaSST"])
    df = pyurof2dsst.processing.load_u_profile()
    ax[0].plot(df.y_R, df.u, "-", label="SST (2-D)")
    df = pyurof2dsst.processing.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, "-", label="SST (2-D)")
    # Load data from 2-D SA case
    os.chdir(cfd_dirs["2-D"]["SpalartAllmaras"])
    df = pyurof2dsa.processing.load_u_profile()
    ax[0].plot(df.y_R, df.u, "-.", label="SA (2-D)")
    df = pyurof2dsa.processing.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, "-.", label="SA (2-D)")
    # Load data from 3-D SST case
    os.chdir(cfd_dirs["3-D"]["kOmegaSST"])
    df = pyurof3dsst.processing.load_u_profile()
    ax[0].plot(df.y_R, df.u, "--", label="SST (3-D)")
    df = pyurof3dsst.processing.load_k_profile()
    ax[1].plot(df.y_R, df.k_total, "--", label="SST (3-D)")
    # Load data from 3-D SA case
    os.chdir(cfd_dirs["3-D"]["SpalartAllmaras"])
    df = pyurof3dsa.processing.load_u_profile()
    ax[0].plot(df.y_R, df.u, ":", label="SA (3-D)")
    df = pyurof3dsa.processing.load_k_profile()
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


def make_perf_bar_charts(theta_0=720, save=False):
    """Create bar charts for C_P and C_D for all cases.

    Parameters
    ----------
    theta_0 : Start angle in degrees for calculating mean performance in the
        CFD cases.
    """
    cp = {}
    cd = {}
    # Load experimental data
    df = load_exp_data()
    cp["Exp."] = df.mean_cp.mean()
    cd["Exp."] = df.mean_cd.mean()
    # Load performance from 2-D SST
    os.chdir(cfd_dirs["2-D"]["kOmegaSST"])
    perf = pyurof2dsst.processing.calc_perf(theta_0=theta_0)
    cp["SST (2-D)"] = perf["C_P"]
    cd["SST (2-D)"] = perf["C_D"]
    # Load performance from 2-D SA
    os.chdir(cfd_dirs["2-D"]["SpalartAllmaras"])
    perf = pyurof2dsa.processing.calc_perf(theta_0=theta_0)
    cp["SA (2-D)"] = perf["C_P"]
    cd["SA (2-D)"] = perf["C_D"]
    # Load performance from 3-D SST
    os.chdir(cfd_dirs["3-D"]["kOmegaSST"])
    perf = pyurof3dsst.processing.calc_perf(theta_0=theta_0)
    cp["SST (3-D)"] = perf["C_P"]
    cd["SST (3-D)"] = perf["C_D"]
    # Load performance from 3-D SA
    os.chdir(cfd_dirs["3-D"]["SpalartAllmaras"])
    perf = pyurof3dsa.processing.calc_perf(theta_0=theta_0)
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
    wm = pyrvatrd.plotting.WakeMap(1.0)
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


def make_recovery_bar_chart(save=False):
    """Create a bar chart with x-labels for each recovery term and 5 different
    bars per term, corresponding to each CFD case and the experimental data.
    """
    data = {}
    # Load recovery terms from 2-D SST case
    os.chdir(cfd_dirs["2-D"]["kOmegaSST"])
    data["SST (2-D)"] = pyurof2dsst.processing.read_funky_log()
    # Load recovery terms from 2-D SA case
    os.chdir(cfd_dirs["2-D"]["SpalartAllmaras"])
    data["SA (2-D)"] = pyurof2dsa.processing.read_funky_log()
    # Load recovery terms from 3-D SST case (0.0 for now)
    os.chdir(cfd_dirs["3-D"]["kOmegaSST"])
    data["SST (3-D)"] = pyurof3dsst.processing.read_funky_log()
    # Load recovery terms from 3-D SA case
    os.chdir(cfd_dirs["3-D"]["SpalartAllmaras"])
    data["SA (3-D)"] = pyurof3dsa.processing.read_funky_log()

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
    import argparse
    parser = argparse.ArgumentParser(description="Create figures.")
    parser.add_argument("plots", nargs="*", help="Which plots to create",
                        choices=["exp_perf", "meancontquiv", "verification",
                                 "kcont", "perf_bar_charts", "profiles",
                                 "recovery", "none"], default="none")
    parser.add_argument("--all", "-a", action="store_true", default=False,
                        help="Plot all figures used in publication")
    parser.add_argument("--style", nargs=1, help="matplotlib stylesheet")
    parser.add_argument("--save", "-s", action="store_true", default=False,
                        help="Save figures to local directory")
    parser.add_argument("--no-show", action="store_true", default=False,
                        help="Do not show figures")
    args = parser.parse_args()
    save = args.save

    if args.plots == "none" and not args.all:
        print("No plots selected")
        parser.print_help()
        sys.exit(2)

    if save:
        if not os.path.isdir("figures"):
            os.mkdir("figures")

    if args.style is not None:
        plt.style.use(args.style)
    else:
        from pxl.styleplot import set_sns
        set_sns()

    if "exp_perf" in args.plots or args.all:
        plot_exp_perf(save=save)
    if "meancontquiv" in args.plots or args.all:
        plot_exp_meancontquiv(save=save)
        plot_cfd_meancontquiv("kOmegaSST", save=save)
        plot_cfd_meancontquiv("SpalartAllmaras", save=save)
    if "verification" in args.plots or args.all:
        plot_verification(save=save)
    if "profiles" in args.plots or args.all:
        plot_profiles(save=save)
    if "perf_bar_charts" in args.plots or args.all:
        make_perf_bar_charts(save=save)
    if "recovery" in args.plots or args.all:
        make_recovery_bar_chart(save=save)
    if "kcont" in args.plots or args.all:
        plot_exp_kcont(save=save)
        plot_cfd_kcont("kOmegaSST", save=save)
        plot_cfd_kcont("SpalartAllmaras", save=save)


    if not args.no_show:
        plt.show()
