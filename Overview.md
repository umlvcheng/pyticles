# Introduction #
The main components of the program are **particle systems**,**forces**,**neighbour lists** and **integrator** and a time stepping algorithm.

## ParticleSystem ##
Contains coordinates, velocities and other properties for a given number (traditionally denoted n) particles, which may vary. Particles' coordinates may be updated in a number of ways, including body forces, interparticle forces, and boundary conditions. A promising way of modelling all of these is the concept of a 'controller', borrowed from Casey Duncan's Lepton.

## NeighbourList ##
A neighbour list tracks interacting pairs of particles from a given ParticleSystem (or in the case of a CouplingNeighbourList from two different particle systems) and maintains 'neighbourly' properties such as interparticle displacements. The list of neighbourly properties depends on the type of particle system. If the particle system has only positions and velocities then the position and velocity differences are of course the only two neighbourly properties. For a SmoothParticleSystem there will be additional properties. As square root operations are expensive it is important to only compute distances as often as necessary.

## Force ##
A force computes rates of change of the particles' properties. If I get the architecture figured out, a force may be a subclass of a generic controller. Most forces are pairwise and in this case the force needs a neighbour list to iterate over. There are pairwise forces that act between particles in the same particle system, and coupling forces that act between different particle systems.

## Controller ##
Anything that mutates the state of the particle is a controller. Forces, collision operators and boundary conditions all qualify.

## Integrator ##
An integrator is a general purpose component that operates on a state vector. The particle class has methods for dumping its properties into a large array, and then retrieving them from the array once the integrator has updated it. These methods do not seem to carry a high overhead, especially when compared to the crushing cost of nbody distance calculations.

## Time Stepper ##
The time stepper applies the controllers to the particle systems.
The particle system must know what Forces to apply to itself. Many forces will be applied using the same NeighbourList, so it is not efficient to create a list for each force. Rather we want to have only one list for each characteristic range. By this I mean that if there is say an electromagnetic force and a gravitational force, both with the same range, we would like them to iterate over the same NeighbourList. If there is also a very short range collision force, it will probably be more efficient to iterate over a list that has been pared down. This is a complex problem that I do not have a full solution to yet.

Time stepping used to be accomplised by the ParticleSytem objects update() method.

## SPAM ##
There may be some smoothed particle type properties that are computed with a longer smoothing length. This may be tricky, although it is probably not likely that the general case of n smoothing lengths will need to be catered for.