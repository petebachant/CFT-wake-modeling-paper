# Response to reviewer 2

We thank the reviewer for his or her very thorough and thoughtful comments,
which have helped us improve the paper.

>In general more work needs to be performed on
• Discussion of mesh factors that may affect the simulation results

Specific comments in the PDF have been addressed in the manuscript and in the
subsection below.

>• Nomenclature, and the lack of definition of many of the variables will cause confusion for many readers

This is a very important point, and we have added many nomenclature definitions
throughout the text.

>• Improvement of figures with nomenclature, labels, axis etc.


>• More explanation of why the various transport properties are investigated and their applicability

These transport properties indicate which terms in the governing equations most
affect wake evolution and its recovery, which will determine rotor spacing in an
array. A comment has been added to the manuscript to clarify this point.

>Additionally the title could be better, maybe add a Computational Fluid Dynamics or simulation somewhere?

Maybe change "modeling" to "simulating"? It is somewhat implied that "RANS"
modeling means it is a computational study, but we understand the reviewer's
point.


## Responses to PDF comments

>Effect of this [slip boundary condition] on the results?

It didn't seem to matter much. The mean velocity fields appear to be nearly
symmetrical about the $x$--$y$ plane, but nonetheless, the slip BC is at least
closer to how a free surface would behave than a no slip BC.

>Any studies proving this - PIV works?

To our knowledge, there aren't any studies directly showing that if CFD results
match well at one point in the domain, they will therefore match elsewhere in
the domain, but if the reviewer knows of any, we'd be happy to reference them.

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

>Wouldnt this have to be a number of complete revolutions?

It virtually is--6.03 revolutions technically, but the additional 0.03
revolutions should not have any appreciable effect on the statistics.

>Is this relevant to the paper [the performance curves]?

This is a valid point. If the reviewer thinks the paper would read okay without
this figure, we would be willing to remove it.

>Why so long [the computational domain]?

We did not perform a mesh dependence study for domain length---only for the
resolution. Since this is a RANS model, the large scale turbulent structures do
not advect downstream like they would in an LES model, as the 3-D vorticity
contours show.

>Or the mesh resolution at 1 diameter downstream [on the difference between the
3-D SA and SST models' mean velocity]?

This shouldn't be a mesh resolution effect between models since the same mesh
was used for each.
