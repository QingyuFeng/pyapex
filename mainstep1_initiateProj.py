# -*- coding: utf-8 -*-
"""
/***************************************************************************
PYAPEX
This program is developed as a standalone scripts to run through 
python console and setup the APEX model. We will remove the requirement of 
an interface and run the model mainly through command line.

This program provides three modes of running:
1. watershed-mode: mode 1
2. boundarywatershed-mode: mode 2

 
1. watershed-mode:
Under this mode, the interface setup the APEX for a watershed. To generate
a watershed, three steps is required. 
The first step is to generate the streamnet.
The second step is to generate the generate watershed based on user 
specified outlet for the interested watershed.
The third step is to generate the apextio and run the model.
After running, a map showing the distribution of runoff, erosion,
total nitrogen and total phosphorus will be generated.
Required input data:
a. dem.tif
b. landuse.tif
c. soil.tif
d. outlet.shp

2. boundaryws-mode
Under this mode, the watershed covered by the boundary will be identified
automatically by the upstream-downstream relationships. Then, an apex model
is setup for each group and run. The result will be for each group.
The paramerters for each subarea will be determined by the major
combination of soil-landuse-slope based on their total area.
The required input will be the same as those in the boundaryhru-mode. 

***************************************************************************/
"""

# Import python standard libraries
import os

# Import the pyapex libraries
from userinputs import userinputs 
from scripts.globalsetting import globalsetting

globalsetting = globalsetting()
userinputs = userinputs()

from scripts.defaultFNFD import defaultFNFD
defaultFNFD = defaultFNFD(userinputs)

if not os.path.isdir(userinputs.fdApexProj):
    os.mkdir(userinputs.fdApexProj)

if not os.path.isdir(userinputs.fdGIS):
    os.chdir(userinputs.fdApexProj)
    os.mkdir(userinputs.fdGIS)

if not os.path.isdir(defaultFNFD.fdTauLayers):
    os.chdir(userinputs.fdApexProj)
    os.mkdir(defaultFNFD.fdTauLayers)

if not os.path.isdir(defaultFNFD.fdApexTio):
    os.chdir(userinputs.fdApexProj)
    os.mkdir(defaultFNFD.fdApexTio)

if userinputs.useDlyWea:
    if not os.path.isdir(defaultFNFD.fdUsrdlylst):
        os.chdir(userinputs.fdApexProj)
        os.mkdir(defaultFNFD.fdUsrdlylst)

if userinputs.userUserLUOPS:
    if not os.path.isdir(userinputs.fdUsrLuOpsFiles):
        os.chdir(userinputs.fdApexProj)
        os.mkdir(userinputs.fdUsrLuOpsFiles)

print("project Setup Done")









