# Response to reviewer 3

Firstly, we'd like to thank the reviewer for his or her thoughtful review. We
appreciate the comments given here, and addressing them has improved the
manuscript significantly.

>1. For convergence study, Fig 5 gives the results for different choice of time step. however, for SST model, the Cp do not convergent with the time step. On the other hand, the choice of time step is always coupled with the choice of space step. Generally speaking, the time step cannot be too small for a certain space discretion condition. Therefore, It is suggested that the author provide this relationship between space and time discretion.

It is true that in general spatial and temporal discretization are coupled.
However, using the PIMPLE solver in OpenFOAM allows for stable solutions even
when the CFL condition is not satisfied in every cell. In our case, we used a
fixed time step, such that it would not be changed by the solver based on the
Courant number. For example, the temporal convergence data shown were acquired
using the "final" spatial resolution and vice versa. This did take some
iterative process, but ultimately we have one independent variable for each
plot. A note has been added to the manuscript to clarify this point.

>2. No the convergence study for 3d model in this paper.

This is true, we did not perform a true convergence study for the 3-D model. We
simply extrapolated the 2-D grid into three dimensions. While this may not be
ideal, this strategy may be useful to practitioners looking to perform similar
simulations, but do not have the computational resources to perform multiple
high fidelity 3-D simulations. The paper has been adjusted to clarify this
point.

>3. In Performance Prediction session, the author gives a figure(Fig.6 ) to show the comparison of 3d , 2d and experimental data. But fig.6 only gives the results for one case for different methods. The 2d method seems over-predict the Cp and Cd. more results of different cases should be given to verify this idea.

For this study we were mainly looking to model the near-wake at peak performance
(determined experimentally), rather than the entire performance envelope. The
performance predictions are therefore an indication of the loading on the
turbine and the level to which it imparts force onto the flow. Notes have been
added to the manuscript to clarify this point.

>4. Shaft and Arm/Strut effects are important to the turbine, and have been discussed by previous publications by using RANS such as
>
Behrouzi F, Malik A M A, Nakisa M, et al. Arm Effect on Performance of Vertical Axis Current Turbine Using RANS Simulation. Applied Mechanics & Materials, 2014, 554(554):531-535.
>
and by using experimental test such as
Li Y, Calisal S M. Three-dimensional effects and arm effects on modeling a vertical axis tidal current turbine. Renewable Energy, 2010, 35(10):2325-2334.
>
However, the authors have not well explained it in the manuscript. Please extend this part.

In the manuscript we have cited a figure from Rawlings (2008, the source of
experimental data used by Li and Calisal for validation), where support strut
drag only accounts for a 4 percentage point decrease in $C_P$, which is much
smaller than the discrepancy observed in the 2-D simulations.
