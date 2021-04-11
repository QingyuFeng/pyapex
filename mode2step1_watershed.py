# -*- coding: utf-8 -*-

"""
In this boundaryhru mode, the following steps will be taken:
1. check whether the layer have same projection
2. TODO: check whether the boundary are covered by the input data
3. generate streamline
4. generate subareas without outlet
5. find subareas covered by the boundary
6. group watershed based on their upstream-downstream relationship

"""
########################################################################################
# Import python standard libraries
import os
from typing import Optional, Tuple, Dict, Set
import pandas as pd
import numpy as np

# Import the pyapex libraries
from scripts.taudemfuncs import taudemfuncs
from scripts.globalsetting import globalsetting
from userinputs import userinputs
from scripts.generalfuncs import generalfuncs
from scripts.gdalfuncs import gdalfuncs
from scripts.graphUtil import graphUtil
from scripts.defaultFNFD import defaultFNFD

globalsetting = globalsetting()
taudemfuncs = taudemfuncs()
userinputs = userinputs()
generalfuncs = generalfuncs()
gdalfuncs = gdalfuncs()
graphUtil = graphUtil()
defaultFNFD = defaultFNFD(userinputs)

########################################################################################
### Workflow to get the waterhsed for boundary #########################################
########################################################################################

if not userinputs.runMode == "mode2":
    print("Please set the run model to mode2 to run this script")
    exit()


########################################################################################
# Input data check: projection and coverage
"""Check existence of dem and boundary data."""
generalfuncs.checkExists(userinputs.fnDem)
generalfuncs.checkExists(userinputs.fnpUsrBdy)

"""check consistency of projection system"""
demProj = gdalfuncs.getRasterProj(userinputs.fnDem)
bdyProj = gdalfuncs.getShpProjGdal(userinputs.fnpUsrBdy)

if not (demProj == bdyProj):
    print("Error: The dem and boundary do not have same projection system.")
    print("Projection for DEM is {}".format(demProj))
    print("Projection for boundary is {}".format(bdyProj))
    exit()


########################################################################################
# Generate watershed
numProcesses = userinputs.numProcessers
mpiexecPath = globalsetting.mpiexecPath
if numProcesses > 0 and (mpiexecPath == '' or not os.path.exists(mpiexecPath)):
    print('Cannot find MPI program {0} so running TauDEM with just one process'.format(mpiexecPath))
    numProcesses = 0

# Running Pit removal
generalfuncs.removeFileifExist(defaultFNFD.fnpFel)
generalfuncs.addToLog("PitFill ...")
taudemfuncs.runPitFill(userinputs.fnDem, 
                            defaultFNFD.fnpFel,
                            numProcesses)   

generalfuncs.removeFileifExist(defaultFNFD.fnpSd8)
generalfuncs.removeFileifExist(defaultFNFD.fnpP)
generalfuncs.addToLog('D8FlowDir ...')
taudemfuncs.runD8FlowDir(defaultFNFD.fnpFel, 
                                defaultFNFD.fnpSd8,
                                defaultFNFD.fnpP,
                                numProcesses)   

generalfuncs.removeFileifExist(defaultFNFD.fnpAd8)
generalfuncs.addToLog('AreaD8 ...')
taudemfuncs.runAreaD8(defaultFNFD.fnpP, 
                                defaultFNFD.fnpAd8,
                                None, None,
                                numProcesses) 

generalfuncs.removeFileifExist(defaultFNFD.fnpGord)
generalfuncs.removeFileifExist(defaultFNFD.fnpPlen)
generalfuncs.removeFileifExist(defaultFNFD.fnpTlen)
generalfuncs.addToLog('GridNet ...') 
taudemfuncs.runGridNet(defaultFNFD.fnpP,
                            defaultFNFD.fnpPlen, 
                            defaultFNFD.fnpTlen, 
                            defaultFNFD.fnpGord, 
                            None, 
                            numProcesses
                            )  

streamThreshold = userinputs.streamThreshold
generalfuncs.removeFileifExist(defaultFNFD.fnpSrcStream)        
generalfuncs.addToLog('Threshold ...')
taudemfuncs.runThreshold(defaultFNFD.fnpAd8, 
                                defaultFNFD.fnpSrcStream, 
                                streamThreshold, 
                                numProcesses) 

generalfuncs.removeFileifExist(defaultFNFD.fnpOrd)        
generalfuncs.removeFileifExist(defaultFNFD.fnpStreamShp)        
generalfuncs.removeFileifExist(defaultFNFD.fnpTree)        
generalfuncs.removeFileifExist(defaultFNFD.fnpCoord)        
generalfuncs.removeFileifExist(defaultFNFD.fnpSubWsFull)        
generalfuncs.addToLog('StreamNet ...')
taudemfuncs.runStreamNet(defaultFNFD.fnpFel, 
                                defaultFNFD.fnpP, 
                                defaultFNFD.fnpAd8,
                                defaultFNFD.fnpSrcStream,
                                None, 
                                defaultFNFD.fnpOrd,
                                defaultFNFD.fnpTree,
                                defaultFNFD.fnpCoord,
                                defaultFNFD.fnpStreamShp,
                                defaultFNFD.fnpSubWsFull,
                                False, 
                                numProcesses)

########################################################################################
# Generate subareas covered by boundary
# Clip the watershed by field boundary
# Convert the clipped tif to asc
# Get unqiue values of the watershed 
generalfuncs.removeFileifExist(defaultFNFD.fnpSubWsUsrBdy)        
generalfuncs.addToLog('Clip Subarea to User Boundary ...')
gdalfuncs.clipRasterbyShp(defaultFNFD.fnpSubWsFull, 
                                userinputs.fnpUsrBdy,
                                defaultFNFD.fnpSubWsUsrBdy
                                )

generalfuncs.removeFileifExist(defaultFNFD.fnpSubWsUsrBdyAsc)        
generalfuncs.addToLog('Convert Sub Boundary to ASC ...')
gdalfuncs.convTif2Asc(defaultFNFD.fnpSubWsUsrBdy,
                            defaultFNFD.fnpSubWsUsrBdyAsc)

# The full subarea map is also converted to asc
generalfuncs.removeFileifExist(defaultFNFD.fnpSubWsAsc)        
generalfuncs.addToLog('Convert Sub Full to ASC ...')
gdalfuncs.convTif2Asc(defaultFNFD.fnpSubWsFull,
                            defaultFNFD.fnpSubWsAsc)

# cif: Contents in file
cifSubFull = gdalfuncs.readASCstr(defaultFNFD.fnpSubWsAsc)
dfSubFull = pd.DataFrame(cifSubFull[3], columns=['subno'])
uniqSubNoFull = dfSubFull['subno'].unique()

cifSubUsrBdy = gdalfuncs.readASCstr(defaultFNFD.fnpSubWsUsrBdyAsc)
dfSubUsrBdy = pd.DataFrame(cifSubUsrBdy[3], columns=['subno'])
uniqSubNoUsrBdy = dfSubUsrBdy['subno'].unique().tolist()

uniqSubNoUsrBdy.remove(cifSubUsrBdy[2])

treeDictFull = graphUtil.readTree(defaultFNFD.fnpTree)

# Either the streamAtt or the tree file has some problem
# of having numbers that does not exist in the demw.
# All the attributes of subareas area processed using
# stream number in the demw file. So, I need to process
# the missing numbers in demw but existing in streamAtt
# or tree file. 
treeDictFixed = graphUtil.rmExtraStrm(uniqSubNoFull, treeDictFull) 

# A graph representing the subareas connection
wsGraph = graphUtil.graphForWS(treeDictFixed)

# A list of subarea numbers that are flowing out
# the field boundaries. These will be used as the
# root of the depth first search to identify the
# watersheds
outletSubUsrBdy = graphUtil.getOutletSubsUsrBdy(uniqSubNoUsrBdy, treeDictFixed)

subGroupWsUsrBdy = graphUtil.groupSubstoWatersheds(wsGraph, outletSubUsrBdy)

# remove watersheds that already contained in other watersheds
# This is done here because we do not know which watersheds has
# more subareas. The reason to do this is to remove extra simulation
# and remove mainly single subarea. 
# This does not happen all the time. It happens most of the time
# because of more than 2 (for example 1, 2, 3 drains to 4).
# There are two situation this happens:
# Taudem to make the rule only at most 2 drains to one downstream. 
# But some times only 1 drains to it, so a extra empty number was
# added. Or the stream was too small or not delineated.
# Other times there are 3 drains to 1. 
# I solved the two situations by removing/reconnecting the streams
# and remove extra watersheds caused by watershed finds by depthfirst
# search algorithms. 
subGroupWsUsrBdy2 = graphUtil.removeExtraWS(subGroupWsUsrBdy)

if not os.path.isdir(defaultFNFD.fdRecWSTif):
    os.mkdir(defaultFNFD.fdRecWSTif)

# reclassify the demw to each watershed for testing
reclassPair = graphUtil.reclassifyWsBdy(subGroupWsUsrBdy2,
     defaultFNFD.fdRecWSTif,
     globalsetting.fnGdalReclassPy,
     defaultFNFD.fnpSubWsFull,
     defaultFNFD.fnpSubRecPair
     )

# # TODO: Need to work with the burn files later. 
# # QSWAT used QGIS, we want to use gdal and see how it can work.
# if userinputs.useburnin:
#     burnFile = userinputs.burnfile
#     if burnFile == '':
#         print('Error: Burn file is not specified!')
#         exit()
#     if not pathlib.Path(burnFile).exists():
#         print('Error: Burn file is not found, please check!')
#         exit()         
    

