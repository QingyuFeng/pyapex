# -*- coding: utf-8 -*-

########################################################################################
# Import python standard libraries
import os

# Import the pyapex libraries
from scripts.taudemfuncs import taudemfuncs
from scripts.globalsetting import globalsetting
from userinputs import userinputs
from scripts.generalfuncs import generalfuncs
from scripts.gdalfuncs import gdalfuncs

globalsetting = globalsetting()
taudemfuncs = taudemfuncs()
userinputs = userinputs()
generalfuncs = generalfuncs()
gdalfuncs = gdalfuncs()

from scripts.defaultFNFD import defaultFNFD
defaultFNFD = defaultFNFD(userinputs)

########################################################################################
### Workflow to get the waterhsed for boundary #########################################
########################################################################################

if not userinputs.runMode == "mode1":
    print("Please set the run model to mode1 to run this script")
    exit()


########################################################################################
generalfuncs.checkExists(userinputs.fnpOutLet)

"""check consistency of projection system"""
demProj = gdalfuncs.getRasterProj(userinputs.fnDem)
oltProj = gdalfuncs.getShpProjGdal(userinputs.fnpOutLet)

if not (demProj == oltProj):
    print("Error: The dem and outlet do not have same projection system.")
    exit()
########################################################################################
# Generate streamline
numProcesses = userinputs.numProcessers
mpiexecPath = globalsetting.mpiexecPath

# Move outlet to streamline to make sure that the outlet is ont the stream cells
generalfuncs.removeFileifExist(defaultFNFD.fnpMvOlt)
generalfuncs.addToLog('moveOutlet to stream line ...')
taudemfuncs.runMoveOutlets(defaultFNFD.fnpP, 
                        defaultFNFD.fnpSrcStream,
                        userinputs.fnpOutLet,
                        defaultFNFD.fnpMvOlt,
                        userinputs.mvOltSnapDist,
                        numProcesses) 

if numProcesses > 0 and (mpiexecPath == '' or not os.path.exists(mpiexecPath)):
    print('Cannot find MPI program {0} so running TauDEM with just one process'.format(mpiexecPath))
    numProcesses = 0

generalfuncs.removeFileifExist(defaultFNFD.fnpAd8)
generalfuncs.addToLog('AreaD8 ...')
taudemfuncs.runAreaD8(defaultFNFD.fnpP, 
                        defaultFNFD.fnpAd8,
                        defaultFNFD.fnpMvOlt,
                        None,
                        numProcesses) 

generalfuncs.removeFileifExist(defaultFNFD.fnpGord)
generalfuncs.removeFileifExist(defaultFNFD.fnpPlen)
generalfuncs.removeFileifExist(defaultFNFD.fnpTlen)
generalfuncs.addToLog('GridNet ...') 
taudemfuncs.runGridNet(defaultFNFD.fnpP,
                        defaultFNFD.fnpPlen, 
                        defaultFNFD.fnpTlen, 
                        defaultFNFD.fnpGord, 
                        defaultFNFD.fnpMvOlt,
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
                        defaultFNFD.fnpMvOlt,
                        defaultFNFD.fnpOrd,
                        defaultFNFD.fnpTree,
                        defaultFNFD.fnpCoord,
                        defaultFNFD.fnpStreamShp,
                        defaultFNFD.fnpSubWsFull,
                        False, 
                        numProcesses)









