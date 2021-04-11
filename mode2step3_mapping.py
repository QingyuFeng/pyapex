# -*- coding: utf-8 -*-

"""
In this mode, the reults include those for each watershed and subarea.
This script will reclassify the watershed maps and generate map results
for them.

"""
########################################################################################
# Import python standard libraries
import os

# Import the pyapex libraries
from userinputs import userinputs
from scripts.generalfuncs import generalfuncs
from scripts.mapUtil import mapUtil
from scripts.globalsetting import globalsetting
from scripts.defaultFNFD import defaultFNFD

generalfuncs = generalfuncs()
userinputs = userinputs()
mapUtil = mapUtil()
globalsetting = globalsetting()
defaultFNFD = defaultFNFD(userinputs)

########################################################################################
### Workflow to set up APEX mode under mode 2 #########################################
########################################################################################
if not userinputs.runMode == "mode2":
    print("Please set the run model to mode2 to run this script")
    exit()

################## Input data check ################################
generalfuncs.checkExists(defaultFNFD.fnpJSONQSNPLvls)

################ get value from MSA #################
# read in files
runSubJs = generalfuncs.readJSON(defaultFNFD.jsonSubSce)
qsnpLvlJs = generalfuncs.readJSON(defaultFNFD.fnpJSONQSNPLvls)
wsRunNames = generalfuncs.readJSON(defaultFNFD.fnpJSONWSRunNames)

subValLvlOut = {}

for wsid, wsRN in wsRunNames.items():
    fnMsa = os.path.join(defaultFNFD.fdApexTio, "{}.MSA".format(wsRN))
    avgAnnVal = None
    avgAnnVal, avgAnnValFWrite = mapUtil.getAvgAnnFromMSA(fnMsa)

    # Then, get the levels of each subarea and variable
    avgAnnLvl, avgAnnLvlFWrite = mapUtil.assignLvls(avgAnnVal, qsnpLvlJs) 

    subValLvlOut[wsid] = {}
    subValLvlOut[wsid]["value"] = avgAnnValFWrite
    subValLvlOut[wsid]["level"] = avgAnnLvlFWrite

    # here wsid: wsXXX
    wsNo = wsid[2:]
    wsKey = "watershed{}".format(wsNo)
    subNoLst = runSubJs[wsKey]['model_setup']['subid_snum']
    
    # Generate source class for reclassify script
    srcClass = mapUtil.getSrcClass(subNoLst)
    
    qLvlLst = mapUtil.getIntValLst(subValLvlOut, "Q", subNoLst, wsid)
    eroLvlLst = mapUtil.getIntValLst(subValLvlOut, "MUSL", subNoLst, wsid)
    tnLvlLst = mapUtil.getIntValLst(subValLvlOut, "TN", subNoLst, wsid)
    tpLvlLst = mapUtil.getIntValLst(subValLvlOut, "TP", subNoLst, wsid)

    fnRecWs = os.path.join(
                    defaultFNFD.fdRecWSTif,
                    'recws{}.tif'.format(wsNo)) 
    generalfuncs.checkExists(fnRecWs)

    # Reclass    
    print("Generating maps for watershed {}".format(wsNo))
    fndestQ = os.path.join(
            defaultFNFD.fdTauLayers,
            'aa{}{}.tif'.format("Q", wsNo))
    generalfuncs.removeFileifExist(fndestQ)
    mapUtil.reclassifyRaster(fnRecWs, fndestQ, srcClass, qLvlLst, globalsetting.fnGdalReclassPy)

    fndestEro = os.path.join(
            defaultFNFD.fdTauLayers,
            'aa{}{}.tif'.format("MUSL", wsNo))
    generalfuncs.removeFileifExist(fndestEro)
    mapUtil.reclassifyRaster(fnRecWs, fndestEro, srcClass, eroLvlLst, globalsetting.fnGdalReclassPy)

    fndestTN = os.path.join(
            defaultFNFD.fdTauLayers,
            'aa{}{}.tif'.format("TN", wsNo))
    generalfuncs.removeFileifExist(fndestTN)
    mapUtil.reclassifyRaster(fnRecWs, fndestTN, srcClass, tnLvlLst, globalsetting.fnGdalReclassPy)

    fndestTP = os.path.join(
            defaultFNFD.fdTauLayers,
            'aa{}{}.tif'.format("TP", wsNo))
    generalfuncs.removeFileifExist(fndestTP)
    mapUtil.reclassifyRaster(fnRecWs, fndestTP, srcClass, tpLvlLst, globalsetting.fnGdalReclassPy)


# Write the output into a json
generalfuncs.writeJSONToFile(defaultFNFD.fnpSubWQQSNPLvls,
                            subValLvlOut)



