# Response to reviewer 2

We thank the reviewer for his or her thoughtful comments, which have helped us
improve the paper.

>In general more work needs to be performed on
• Discussion of mesh factors that may affect the simulation results


>• Nomenclature, and the lack of definition of many of the variables will cause confusion for many readers


>• Improvement of figures with nomenclature, labels, axis etc.


>• More explanation of why the various transport properties are investigated and their applicability


>Additionally the title could be better, maybe add a Computational Fluid Dynamics or simulation somewhere?


## Responses to PDF comments

>Effect of this [slip boundary condition] on the results?

It didn't seem to matter much. The mean velocity fields appear to be nearly
symmetrical about the $x$--$y$ plane, but nonetheless, the slip BC is at least
closer to how a free surface would behave than a no slip BC.

>Is this mesh [Figure 4] too coarse for adequate resolution of the flow?

It could be. For our mesh dependence study we held the topology fixed and scaled
the mesh proportionally. The mesh should be fine enough to resolve the boundary
layer since $y^+ \sim 1$, but it is a fair point that maybe separated flow
structures may be dissipated in an exaggerated way. However, exploring the mesh
topology parameter space would have been prohibitive.

>So the SA and SST took the same time?

Since the chosen SA time step was about half that of the SST, the SA model did
take longer to solve, though they were still the same order of magnitude. We
decided it wouldn't be useful to readers to give very specific metrics of solver
time since there could be many intervening variables, e.g., hardware.

>Did you prove that the meshing of the outer walls didn't affect the results.

We did not, but if we inspect the velocity fields, which don't extend out all
the way to the walls, gradients are very small around the outer region,
indicating the effects should be negligible.

>why approximately [rotor performance periodicity]?

Since this is an unsteady simulation, there are interactions between blade wakes
that are not perfectly periodic, so there are some minor differences between
rotor revolutions. Note that this is consistent with the experimental results.

>Why blank? [viscous transport in Figure 12]

These terms aren't zero, but are extremely small.

>Not sure if this is true - DMS models have tip correction factors - see reference #2?

We could not find any instances in this reference for DMS model tip correction
factors for VAWTs. However, if the reviewer has a specific correction in mind we
would be happy to note this in the manuscript.

>Can you show differences between these graphically, i.e subtract B from A and C from A to show the change - this would make it a lot easier to see differences

We did try computing "difference" plots, but these were a bit noisy and were
difficult to interpret.
