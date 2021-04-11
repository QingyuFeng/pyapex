# -*- coding: utf-8 -*-
import math
import pandas as pd
import os

class mapUtil():

    def __init__(self):

        self.demo = ""



    #######################################################
    @staticmethod
    def getSceWSList(runSubJs, sceLst):
        """
        This function get the name list of the MSA file.
        """
        msaNameLst = []
        for wsid in range(len(runSubJs.keys())):
            for sceKey, sceNm in sceLst.items():
                temp = ""
                temp = "{}_{}".format(sceNm["sname"], wsid+1) 
                msaNameLst.append(temp)
            
        return msaNameLst

    #######################################################
    @staticmethod
    def getAvgAnnFromMSA(fnMsa):

        fid = open(fnMsa, 'r')
        lif = fid.readlines()
        fid.close()
        
        # The first 10 lines are heads and we do not need it
        del(lif[0:10])
        
        # Separate the lines in each line and then put it into
        # a dataframe
        # create a dataframe to store the info.
        dfmsa = None
        
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split(' ')
            while '' in lif[lidx]:
                lif[lidx].remove('')
            lif[lidx][-1] = lif[lidx][-1][:-1]
            
            for idx2 in range(5, len(lif[lidx])-1):
                if math.isnan(float(lif[lidx][idx2])):
                    lif[lidx][idx2] = 0.00
                else:
                    lif[lidx][idx2] = float(lif[lidx][idx2])

        labels = ["OrderNO", "SubNO", "YearXXXX",
                    "YearOrder", "OutVar", "Jan",
                    "Feb", "Mar", "Apr", "May",
                    "June", "July", "Aug",  "Sept",
                    "Oct", "Nov", "Dec", "YearSum", "OutVar2"]

        dfmsa = pd.DataFrame.from_records(lif, columns=labels) 
        dict_subvarannavg = None
        dict_subvarannavg = dfmsa[['SubNO', 'OutVar',"YearSum"
            ]].groupby(['SubNO','OutVar'])['YearSum'].mean().to_dict()
            
        # Calculate the TN and TP
        # Now we get the average annual values for each variable
        # at each subarea. But we need to add two more, the total nitrogen
        # and total phosphorus
        # Current variables include
        # [PRCP, Q, QDR,MUSL, QN, YN, SSFN, PRKN, QDRN
        #  YP, QP, QDRP, QRFN, MNP, YPM, YPO]
        # Loop through the subareas
        subnolst = None
        subnolst = dfmsa['SubNO'].unique()
        
        for subid in subnolst:
            dict_subvarannavg[(subid,"TN")] = [
                    dict_subvarannavg[(subid,"QN")]
                    + dict_subvarannavg[(subid,"YN")]
                    + dict_subvarannavg[(subid,"SSFN")]
                    + dict_subvarannavg[(subid,"PRKN")]
                    + dict_subvarannavg[(subid,"QDRN")]][0]
            dict_subvarannavg[(subid,"TP")] = [
                    dict_subvarannavg[(subid,"YP")]
                    + dict_subvarannavg[(subid,"QP")]
                    + dict_subvarannavg[(subid,"SSFN")]
                    + dict_subvarannavg[(subid,"PRKN")]
                    + dict_subvarannavg[(subid,"QDRN")]][0]
        
        #dict_subvarannmax = dfmsa[['SubNO', 'OutVar',"YearSum"
        #    ]].groupby(['SubNO','OutVar'])['YearSum'].max().to_dict()

        # Modify the key from tuple to string for write to file 
        newDict = {}

        for key, value in dict_subvarannavg.items():
            newKey = "{}_{}".format(key[0], key[1])
            newDict[newKey] = value

        return dict_subvarannavg, newDict 


    #######################################################
    def assignLvls(self, avgAnnVal, lvlJs):

        lvlDict = {} 

        for key, value in avgAnnVal.items():

            if key[1] =="Q":  
                lvlDict[key] = self.determineLvls(value, "runoff", lvlJs)
            elif key[1] =="MUSL":
                lvlDict[key] = self.determineLvls(value, "soilerosion", lvlJs)
            elif key[1] =="TN":
                lvlDict[key] = self.determineLvls(value, "nitrogen", lvlJs)
            elif key[1] =="TP":
                lvlDict[key] = self.determineLvls(value, "phosphorus", lvlJs)

        # Modify the key from tuple to string for write to file
        newDict = {}
        for key, value in lvlDict.items():
            newKey = "{}_{}".format(key[0], key[1])
            newDict[newKey] = value


        return lvlDict, newDict



    #######################################################
    def determineLvls(self, valToCheck, varKey, lvlJs):
        
        varLvl = lvlJs[varKey]

        for lvlKey, lvlDtl in varLvl.items(): 
            if self.checkinbetween(valToCheck, lvlDtl["min"], lvlDtl["max"]):    
                return lvlKey[5:]
                


    #######################################################
    def checkinbetween(self, val, valmin, valmax):
            
        if ((val >= valmin) and (val < valmax)):
            return True
        else:
            return False


    #######################################################
    @staticmethod
    def getIntValLst(subValLvl, varName, subNoLst, sceWS):

        valLvlDict = subValLvl[sceWS]["value"] 

        intValLst = []
        for subId in subNoLst:
            key = "{}_{}".format(subId, varName)
            intVal = str(int(round(valLvlDict[key]+0.5, 0)))
            intValLst.append(intVal)
        return intValLst


    #######################################################
    @staticmethod
    def getLvlLst(subValLvl, varName, subNoLst, sceWS):

        valLvlDict = subValLvl[sceWS]["level"] 

        lvlLst = []
        for subId in subNoLst:
            key = "{}_{}".format(subId, varName)
            lvlLst.append(valLvlDict[key])
        return lvlLst


    #######################################################
    @staticmethod
    def getSrcClass(subNoLst):

        newLst = []
        for subId in subNoLst:
            newLst.append("=={}".format(subId))

        return newLst


    #######################################################
    @staticmethod
    def reclassifyRaster(srcrast, destrast, srcClass, destClass, gdalrecpyfile):

        """
        # gdal_reclassify.py [-c source_classes] [-r dest_classes] [-d default] [-n default_as_nodata] src_dataset dst_dataset

        Example of using the tool:
        python gdal_reclassify.py source_dataset.tif destination_dataset.tif -c "<30, <50, <80, ==130, <210"
        -r "1, 2, 3, 4, 5" -d 0 -n true -p "COMPRESS=LZW"

        Steps include:
        1. generate the source classes
        2. generate the dest_classes
        3. generate the command
        4. run the command

        """

        srcclasses = ",".join(srcClass)
        destclasses = ",".join(destClass)

        # Delete dest file if exist:
        if (os.path.exists(destrast)):
            os.remove(destrast)

        # Then generate command
        cmd1 = ['python '
            + gdalrecpyfile
            + ' '
            + srcrast
            + ' '
            + destrast
            + ' -c "'
            + srcclasses
            + '" -r "'
            + destclasses
            + '" -d 0 -n true']

        os.system(cmd1[0])

