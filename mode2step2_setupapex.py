# -*- coding: utf-8 -*-

"""
In this boundaryhru mode, the following steps will be taken:
1. Check existence and projection of land use and soil, and clip to extent
2. Convert whole watershed (all subs) from tif to shape for centroid.
3. Convert tifs to ascs for calculating APEX inputs
4. Calculate APEX inputs from ASCs
5. Write Soil
6. Write Climate
7. Write site
8. Write Sub
9. Write cont
10.Write Run
11. Copy other files
12. Runs APEX

"""
########################################################################################
# Import python standard libraries
import os
from shutil import copyfile
import copy

# Import the pyapex libraries
from userinputs import userinputs
from scripts.generalfuncs import generalfuncs
from scripts.gdalfuncs import gdalfuncs
from scripts.apexfuncs import apexfuncs
from scripts.ascInfoBdy import ascInfoBdy
from scripts.subWsInfoBdy import subWsInfo
from scripts.solfuncs import solfuncs
from scripts.sqldbfuncs import sqldbfuncs
from scripts.climfuncs import climfuncs
from scripts.globalsetting import globalsetting
from scripts.defaultFNFD import defaultFNFD

userinputs = userinputs()
generalfuncs = generalfuncs()
gdalfuncs = gdalfuncs()
apexfuncs = apexfuncs()
solfuncs = solfuncs()
sqldbfuncs = sqldbfuncs()
climfuncs = climfuncs()
globalsetting = globalsetting()
defaultFNFD = defaultFNFD(userinputs)

########################################################################################
### Workflow to set up APEX mode under mode 2 #########################################
########################################################################################
if not userinputs.runMode == "mode2":
    print("Please set the run model to mode2 to run this script")
    exit()


################## Input data check ################################
generalfuncs.checkExists(userinputs.fnLandUse)
generalfuncs.checkExists(userinputs.fnSoil)

demProj = gdalfuncs.getRasterProj(userinputs.fnDem)
landuseProj = gdalfuncs.getRasterProj(userinputs.fnSoil)
soilProj = gdalfuncs.getRasterProj(userinputs.fnLandUse)

if not (demProj == landuseProj):
    print("Error: The projection of the LANDUSE layer is not \
            consistent with that of the DEM layer.")
    exit()
if not (demProj == soilProj):
    print("Error: The projection of the SOIL layer is not \
            consistent with that of the DEM layer.")
    exit()

################ Cut landuse and soil to WS extent #################
subWsFullExt = gdalfuncs.getRasterExtent(defaultFNFD.fnpSubWsFull)
print('Clipping Landuse Data to watershed boundary ...')
generalfuncs.addToLog('Clipping Landuse Data to watershed boundary ...')
generalfuncs.removeFileifExist(defaultFNFD.fnpWsExtLu)   
gdalfuncs.clipRasterbyExtent(userinputs.fnLandUse, 
                                subWsFullExt,
                                defaultFNFD.fnpWsExtLu)
print('Clipping Soil Data to watershed boundary ...')
generalfuncs.addToLog('Clipping Soil Data to watershed boundary ...')
generalfuncs.removeFileifExist(defaultFNFD.fnpWsExtSoil)   
gdalfuncs.clipRasterbyExtent(userinputs.fnSoil, 
                                subWsFullExt,
                                defaultFNFD.fnpWsExtSoil)

################ Convert WSBdy from tiff to shp #################
generalfuncs.removeFileifExist(defaultFNFD.fnpSubWsShp)   
print('Convert watershed raster to shapefile ...')
generalfuncs.addToLog('Convert watershed raster to shapefile ...')
gdalfuncs.convtif2shp(defaultFNFD.fnpSubWsFull, defaultFNFD.fnpSubWsShp)
print('Convert plen raster to asc ...')
generalfuncs.removeFileifExist(defaultFNFD.fnpPlenAsc)
gdalfuncs.convTif2Asc(defaultFNFD.fnpPlen,
                            defaultFNFD.fnpPlenAsc)
print('Convert dem raster to asc ...')
generalfuncs.removeFileifExist(defaultFNFD.fnpDemASC)
gdalfuncs.convTif2Asc(defaultFNFD.fnpFel,
                            defaultFNFD.fnpDemASC)
print('Convert landuse raster to asc ...')
generalfuncs.removeFileifExist(defaultFNFD.fnpWsExtLuAsc)
gdalfuncs.convTif2Asc(defaultFNFD.fnpWsExtLu,
                            defaultFNFD.fnpWsExtLuAsc)
print('Convert soil raster to asc ...')
generalfuncs.removeFileifExist(defaultFNFD.fnpWsExtSolAsc)
gdalfuncs.convTif2Asc(defaultFNFD.fnpWsExtSoil,
                            defaultFNFD.fnpWsExtSolAsc)
print('Convert stream raster to asc ...')
generalfuncs.removeFileifExist(defaultFNFD.fnpSrcStreamAsc)
gdalfuncs.convTif2Asc(defaultFNFD.fnpSrcStream,
                            defaultFNFD.fnpSrcStreamAsc)
print('Convert slope raster to asc ...')
generalfuncs.removeFileifExist(defaultFNFD.fnpSd8Asc)
gdalfuncs.convTif2Asc(defaultFNFD.fnpSd8, defaultFNFD.fnpSd8Asc)

################ Extract ASC info to field subarea json #################
# Copy template variable json to run folder
copyfile(defaultFNFD.jsonVarSubWsTemp, defaultFNFD.jsonVarSubWsSce)
copyfile(defaultFNFD.jsonSitTemp, defaultFNFD.jsonSitSce)
print('Extracting information from asc files ...')
ascInfoBdy = ascInfoBdy(defaultFNFD)
## Json file storing all necessary variables
# After getting the information for routing, it is time
# to process the information into the json files.
subWsVarJSON = generalfuncs.readJSON(defaultFNFD.jsonVarSubWsSce)
sitJSON = generalfuncs.readJSON(defaultFNFD.jsonSitSce)

# Create a dictionary that have required number of watersheds
# in the dictionary
for wsk, wsv in ascInfoBdy.wssubflddict.items():
    wsjsonkey = 'watershed%s' %(wsk)
    subWsVarJSON[wsjsonkey] = subWsVarJSON['tempws']

# If key is not present in dictionary, then del can throw KeyError
del(subWsVarJSON["tempws"])
print('Calculating subarea variable value from asc data ...')
wsvarjson2 = {}
# Then, updating the json file
for wsid2 in range(len(ascInfoBdy.wssubflddict)):
    tempSubWsInfo = None
    tempSubWsInfo = subWsInfo(str(wsid2+1), ascInfoBdy)

    wsjsonkey2 = 'watershed%i' %(wsid2+1)
    # Update the json file
    ascInfoBdy.wsSubCtr,ascInfoBdy.wsSubSolOpsLatLon = tempSubWsInfo.modifywsJSON(
            wsid2,
            subWsVarJSON,
            ascInfoBdy.wsSubCtr,
            ascInfoBdy.wsSubSolOpsLatLon,
            tempSubWsInfo.subPurePath,
            tempSubWsInfo.subRouting,
            ascInfoBdy
            )

    wsvarjson2[wsjsonkey2] = copy.deepcopy(subWsVarJSON[wsjsonkey2])

# Update site json information
sitJSON = apexfuncs.updatejson_sit(sitJSON, wsvarjson2)

# Write the information into a json file
generalfuncs.writeJSONToFile(defaultFNFD.jsonSubSce, wsvarjson2)
generalfuncs.writeJSONToFile(defaultFNFD.jsonSubWsSolLuLL,
                            ascInfoBdy.wsSubSolOpsLatLon)
generalfuncs.writeJSONToFile(defaultFNFD.jsonSitSceRun, sitJSON)

################ Write APEX files: sol #################
# Copy template sol json to run folder
copyfile(defaultFNFD.jsonSolTemp,  defaultFNFD.jsonSolSce)
print('preparing apex input data: soil ...')
# Call soil function to write the SOLCOM file
solfuncs.writeSolCOM(defaultFNFD.fdApexTio,
            defaultFNFD.jsonSubWsSolLuLL,
            defaultFNFD.fnpSolCom)

# Create a runsol.json as a template soil json conatining
# template for each soil. The value will be updated in the
# next step.
# Updating nested value in Python is not running correct, I will create
# an empty dictionary, update the value, and then combine them.
# Read in two json files
# Read in the soillu for watershed json
sollujson = generalfuncs.readJSON(defaultFNFD.jsonSubWsSolLuLL)       
tmpSolJSON = generalfuncs.readJSON(defaultFNFD.jsonSolSce)

solListAll = []
for k, v in sollujson.items():
    if not v['mukey'] in solListAll:
        solListAll.append(v['mukey'])

# An empty template json to store all updated json
allUpdatedSolJSON = {}

# Determine the soil database and table to be used
if not userinputs.useUserSoil:
    fnDbSoil = defaultFNFD.dbfnCliSol
    fnTbSoil = defaultFNFD.tbDftSoil
else:
    fnDbSoil = userinputs.dbUsrSoil
    fnTbSoil = userinputs.tbUsrSoil    

for solid in solListAll:
    # Update the variable
    temp1sol = None
    temp1sol = copy.deepcopy(tmpSolJSON)
    temp1sol = solfuncs.update1soljson(fnDbSoil,
                                        "soil1", 
                                        solid,
                                        temp1sol,
                                        fnTbSoil)
    allUpdatedSolJSON[solid] = temp1sol["soil1"]

generalfuncs.writeJSONToFile(defaultFNFD.jsonSolSceRun, allUpdatedSolJSON)

# Transfer the runsol json into APEXSOL files
for mkey, solvalue in allUpdatedSolJSON.items():
    solfuncs.writejson2sol(defaultFNFD.fdApexTio, 
                            solvalue)

################ Write APEX files: cli #################
print('preparing apex input data: climate ...')
# Get the latitude and longitude of the watershed 
solLuLatLon = generalfuncs.readJSON(defaultFNFD.jsonSubWsSolLuLL)
# A container of unique station names
allMonStns = []
for subno, subinfo in solLuLatLon.items():
    generalfuncs.removeFileifExist(defaultFNFD.fnFoundStn)
    climfuncs.getCliNearStn(subinfo["lon"], 
                            subinfo["lat"],
                            defaultFNFD.fdApexTio,
                            globalsetting.fnclisearch,
                            defaultFNFD.fnpMonStnListdb)
    stninfo = None
    stninfo = climfuncs.getFoundStnInfo(defaultFNFD.fnFoundStn)
        
    if not stninfo[1] in allMonStns:
        allMonStns.append(stninfo[1])

# Write the station com files required by apex
# Create a list to store all stations in the db file as a dict
# will be used to get the information and write stn com files.
monStnInfodb = climfuncs.readweastndb2dict(defaultFNFD.fnpMonStnListdb)
climfuncs.writeapexcom(
                defaultFNFD.fnapexwndcom,
                monStnInfodb,
                allMonStns,
                "WND"
                )
climfuncs.writeapexcom(
                defaultFNFD.fnapexwp1com,
                monStnInfodb,
                allMonStns,
                "WP1"
                )

# Write wp1 file:
for wstnidx in range(len(allMonStns)):
    stnname = None
    stnname = allMonStns[wstnidx]
    climfuncs.writewp1file(
            defaultFNFD.dbfnCliSol,
            stnname,
            defaultFNFD.fdApexTio,
            defaultFNFD.tbwgncfsr)
    climfuncs.writewndfile(
            defaultFNFD.dbfnCliSol,
            stnname,
            defaultFNFD.fdApexTio,
            defaultFNFD.tbwgncfsr)    

if userinputs.useDlyWea:
    allDlyStns = []
    for subno, subinfo in solLuLatLon.items():
        generalfuncs.removeFileifExist(defaultFNFD.fnFoundStn)
        climfuncs.getCliNearStn(subinfo["lon"], 
                                subinfo["lat"],
                                defaultFNFD.fdApexTio,
                                globalsetting.fnclisearch,
                                userinputs.fnUserDlyListdb)
        stninfo = None
        stninfo = climfuncs.getFoundStnInfo(defaultFNFD.fnFoundStn)
        if not stninfo[1] in allDlyStns:
            allDlyStns.append(stninfo[1])

    dlyStnInfodb = climfuncs.readweastndb2dict(userinputs.fnUserDlyListdb)
    # Write dly com file
    climfuncs.writeapexcom(
                    defaultFNFD.fnapexdlycom,
                    dlyStnInfodb,
                    allDlyStns,
                    "DLY")

    # Copy dly file 
    for dlyIdx in allDlyStns:
        srcDly = os.path.join(userinputs.fdUserDly,
            "{}.DLY".format(dlyIdx))
        if not os.path.isfile(srcDly):
            print("""DLY file {} does not exist! Please put it under the {} folder!
                    and put the DLY name in the dly list file.""".format(
                srcDly, userinputs.fdUserDly))
            exit()
        else:
            destDly = os.path.join(defaultFNFD.fdApexTio,
                "{}.DLY".format(dlyIdx))
            copyfile(srcDly, destDly)
# If not using user daily weather, copy a demo empty one
else:
    copyfile(defaultFNFD.fnapexdlycomTemp, defaultFNFD.fnapexdlycom)

################ Write APEX files: site and com #################
generalfuncs.removeFileifExist(defaultFNFD.fnpSITCOM)
generalfuncs.removeFileifExist(defaultFNFD.fnpSIT)
apexfuncs.writeSITCOMandFile(defaultFNFD.jsonSitSceRun, 
                            defaultFNFD.fnpSITCOM,
                            defaultFNFD.fnpSIT)

################ Write APEX files: sub and com #################
subJSON = generalfuncs.readJSON(defaultFNFD.jsonSubSce)
generalfuncs.removeFileifExist(defaultFNFD.fnSubAllCOM)

fidsubcom = open(defaultFNFD.fnSubAllCOM, "w")
for wsid in range(len(subJSON.keys())):
    fidsubcom.writelines("%5i\tSUB%s.SUB\n" %(wsid+1, wsid+1))
fidsubcom.close()

# Write the individual subarea files
for key, value in subJSON.items():
    wsid = key[9:]
    apexfuncs.writefile_sub(wsid, value, defaultFNFD.fdApexTio)

################ Write APEX files: CONT #################
print('preparing apex input data: control ...')
generalfuncs.removeFileifExist(defaultFNFD.jsonContRun)
copyfile(defaultFNFD.jsonContTemp, defaultFNFD.jsonContRun)
generalfuncs.removeFileifExist(defaultFNFD.fnpCont)
apexfuncs.writeAPEXCONT(defaultFNFD.jsonContRun, defaultFNFD.fnpCont, userinputs.dailyWeaVar, userinputs.useDlyWea)

################ Write APEX files: OPSCCOM #################
print('preparing apex input data: management ...')
apexfuncs.writeOPSCOM(defaultFNFD.jsonSubWsSolLuLL, defaultFNFD.fnpOPSCOM)
apexfuncs.copyOPSFiles(defaultFNFD.fdopssrc, defaultFNFD.fdApexTio)

################ Write APEX files: RUN #################
print('preparing apex input data: run file ...')
generalfuncs.removeFileifExist(defaultFNFD.fnpAPEXRUN)
runWSNames = apexfuncs.writeAPEXRUN(defaultFNFD.jsonSubSce, defaultFNFD.fnpAPEXRUN, userinputs.fnApexProj)
generalfuncs.writeJSONToFile(defaultFNFD.fnpJSONWSRunNames,
                            runWSNames)

################ Write APEX files: Database #################
apexfuncs.copyDataBaseFILE(globalsetting.fnapexbin, defaultFNFD.fdApexTio, defaultFNFD.fdApexData)

################ Run APEX #################
print('Run APEX model ...')
apexfuncs.runAPEX1501(defaultFNFD.fdApexTio, userinputs.fdApexProj)

