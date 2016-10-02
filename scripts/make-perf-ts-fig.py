#!/usr/bin/env python
"""Create performance coefficient time series plot."""

from __future__ import division, print_function
from pxl.styleplot import set_sns
import matplotlib.pyplot as plt
import pandas as pd
import sys


set_sns(context="paper")

fpath = "UNH-RVAT-3D-OpenFOAM/processed/perf.csv"

df = pd.read_csv(fpath)

fig, ax = plt.subplots()

ax.plot(df.theta_deg, df.cp)

ax.set_xlabel(r"$\theta$ (degrees)")
ax.set_ylabel("$C_P$")
ax.set_ylim((0, 0.8))

fig.tight_layout()

fig.savefig("figures/cp-time-series.pdf")

if "--show" in sys.argv:
    plt.show()
