# equidistance

====

Video : https://dl.dropboxusercontent.com/u/42218552/equidistance.mp4

====

This is a simulation of a complex system. 

Consider n points on a two dimensional plane. Each point is assigned to two targets and must attempt to stay equidistant to both targets. At every timestep, it moves to achieve this goal. In addition, this simulation also adds two constraints the points to prevent them from moving two close to each other and from moving two far from the origin. 

These constraints allows this simulation to mimic the system when it is performed with humans instead of points. The resulting system has a chaotic behavior and oscillates between states of relative stability and states of higher activity.

If the potential function is adjusted so that the points are insensitive to small differences in distance, then the resulting system converges to a static state after a short period of time.

If the simulation is adjusted so that all the points coordinate greedily to a equilibrium-state, equilibrium is also quickly achieved.
