#! /usr/local/bin/python

""" 
    Batch script for Smooth Particle solver. 
    Copyright Andrew Charles 2010
    All rights reserved.
"""

import sys
from time import time
import particles
import forces
import neighbour_list
from properties import spam_properties
from spam_nc import create_sph_ncfile, write_step
import spam_complete_force
import numpy as np

# Global variables
MAX_STEPS = 50000
NDIM = 3
XMAX = 12 
YMAX = 12
ZMAX = 12
VMAX = 0.0
dt = 0.05
SPACING = 1.0
LIVE_VIEW = False
SIDE = (10,10,10)
NP = SIDE[0] * SIDE[1] * SIDE[2]
TEMPERATURE = 1.5
HLONG = 5.0
HSHORT = 2.5

ofname = 'output.nc'

print "Initialising"
p = particles.SmoothParticleSystem(NP,maxn=NP,d=3,rinit='grid',vmax=VMAX
,side=SIDE,spacing=SPACING,xmax=XMAX,ymax=YMAX,zmax=ZMAX
,temperature=TEMPERATURE,hlong=HLONG,hshort=HSHORT,
thermostat_temp=TEMPERATURE,thermostat=True)
nl = neighbour_list.VerletList(p,cutoff=5.0)
p.nlists.append(nl)
p.nl_default = nl
p.forces.append(spam_complete_force.SpamComplete(p,nl))
p.forces.append(forces.FortranCollisionForce(p,nl,cutoff=0.5))
nl.build()
nl.separations()
spam_properties(p,nl)
cnt = 0
attribs = {'name':'Andrew', 'age':33}
create_sph_ncfile(ofname,attribs,NP,NDIM)
initialise()
print "STEP   INT  DERIV =  PAIR + SPAM +  FORCE   "
for i in range(MAX_STEPS):
    tstart = time()
    p.update(dt)
    if np.isnan(p.r).any():
        print 'stopping due to nan'
        break
    if i % 10 == 0:
        write_step(ofname,p)
print 'Completed',i,'steps'


