# -*- coding: utf-8 -*-

"""
In this watershed mode, the following steps will be taken:
1. generate streamline
2. generate subareas without outlet
3. find subareas covered by the boundary
4. group watershed based on their upstream-downstream relationship
"""

########################################################################################
# Import python standard libraries
import os

# Import the pyapex libraries
from scripts.taudemfuncs import taudemfuncs
from scripts.globalsetting import globalsetting
from userinputs import userinputs
from scripts.generalfuncs import generalfuncs
from scripts.defaultFNFD import defaultFNFD

globalsetting = globalsetting()
taudemfuncs = taudemfuncs()
userinputs = userinputs()
generalfuncs = generalfuncs()
defaultFNFD = defaultFNFD(userinputs)

########################################################################################
### Workflow to get the waterhsed for boundary #########################################
########################################################################################

if not userinputs.runMode == "mode1":
    print("Please set the run model to mode1 to run this script")
    exit()


########################################################################################
# Input data check: projection and coverage
generalfuncs.checkExists(userinputs.fnDem)

########################################################################################
# Generate streamline
numProcesses = userinputs.numProcessers
mpiexecPath = globalsetting.mpiexecPath
if numProcesses > 0 and (mpiexecPath == '' or not os.path.exists(mpiexecPath)):
    print('Cannot find MPI program {0} so running TauDEM with just one process'.format(mpiexecPath))
    numProcesses = 0

# Running Pit removal
generalfuncs.removeFileifExist(defaultFNFD.fnpFel)
generalfuncs.addToLog("PitFill ...")
ok = taudemfuncs.runPitFill(userinputs.fnDem, 
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
ok = taudemfuncs.runAreaD8(defaultFNFD.fnpP, 
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









