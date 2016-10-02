#!/usr/bin/env python
"""Create performance coefficient time series plot."""

from __future__ import division, print_function
from pxl.styleplot import set_sns
import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np

set_sns(context="paper")

fpath = "UNH-RVAT-3D-OpenFOAM/processed/perf.csv"

df = pd.read_csv(fpath)

# Create revolution-averaged data
nrevs = int(df.theta_deg.max() / 360)
rev = []
cp_rev_ave = []
for n in range(nrevs):
    rev.append(n + 1)
    cp_rev_ave.append(
        df.cp[np.logical_and(df.theta_deg >= n*360,
                             df.theta_deg < (n + 1)*360)].mean()
    )

fig, ax = plt.subplots()

ax.plot(rev, cp_rev_ave, marker="o")

ax.set_xlabel(r"Rotor revolution")
ax.set_ylabel("$C_P$")
# ax.set_ylim((0, 0.8))

fig.tight_layout()

fig.savefig("figures/cp-time-series.pdf")

if "--show" in sys.argv:
    plt.show()
