#! /usr/local/bin/python

""" 
    Batch script for Smooth Particle solver. 
    Copyright Andrew Charles 2009
    All rights reserved.
"""

import sys
from time import time
import particles
import c_forces as forces
import neighbour_list
from properties import spam_properties
from spam_nc import create_sph_ncfile, write_step

# Global variables
MAX_STEPS = 10
NP = 125
NDIM = 3
XMAX = 8 
YMAX = 8
ZMAX = 8
VMAX = 0.0
dt = 0.05
SPACING = 0.9
LIVE_VIEW = False
SIDE = (5,5,5)
TEMPERATURE = 1.8
HLONG = 4.0
HSHORT = 2.0
ofname = 'output.nc'

p = particles.SmoothParticleSystem(NP,maxn=NP,d=3,rinit='grid',vmax=VMAX
    ,side=SIDE,spacing=SPACING,xmax=XMAX,ymax=YMAX,zmax=ZMAX)

def initialise():
    global p
    print "Initialising"
    p = particles.SmoothParticleSystem(NP,maxn=NP,d=3,rinit='grid',vmax=VMAX
        ,side=SIDE,spacing=SPACING,xmax=XMAX,ymax=YMAX,zmax=ZMAX
        ,temperature=TEMPERATURE,hlong=HLONG,hshort=HSHORT)

    nl = neighbour_list.SortedVerletList(p,cutoff=4.0)
    p.nlists.append(nl)
    p.nl_default = nl
    p.forces.append(forces.SpamForce(p,nl))
    p.forces.append(forces.CohesiveSpamForce(p,nl))
    nl.build()
    nl.separations()
    spam_properties(p,nl,p.h,p.hlr)
    cnt = 0
    attribs = {'name':'Andrew', 'age':33}
    create_sph_ncfile(ofname,attribs,NP,NDIM)

if __name__ == "__main__":
    initialise()
    print "STEP   INT  DERIV =  PAIR + SPAM +  FORCE   "
    for i in range(MAX_STEPS):
        tstart = time()
        p.update(dt)
        write_step(ofname,p)
        print "%5.3f  " %(time() - tstart)             \
             + "%5.3f  " %(p.timing['integrate time']) \
             + "%5.3f  " %(p.timing['deriv time'])     \
             + "%5.3f  " %(p.timing['pairsep time'])   \
             + "%5.3f  " %(p.timing['SPAM time'])     \
             + "%5.3f  " %(p.timing['force time'])
    
