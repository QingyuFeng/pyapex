# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import json, copy

from .gdalfuncs import gdalfuncs
from .graphUtil import graphUtil

gdalfuncs = gdalfuncs()
graphUtil = graphUtil()


class ascInfoBdy():

    def __init__(self, userInput):
        """Constructor."""
        # Slope group to be modified. Included here for
        # Future reference
        self.slopeGroup = userInput.usrslpgroup

        # A temporary to store the classes of each watershed
        self.wsSubinfoClasses = {}
        # A continuous counter starting from subarea 1 to watershed
        # 1, to the last one. This will be used to write the list files.
        self.wsSubCtr = 0

        # A dictionary to store the ws_subno, soil, landuse,
        # latitude, longitude. The ws_subno will be the order
        # number of the list in soil, management, and daily weather
        # station.
        self.wsSubSolOpsLatLon = {}

        # wssubflddict: A dictionary to store the lines
        # in the wssubfld. Each line contains the subareas
        # in one watershed covered by the field.
        self.wssubflddict = self.readWsSubFlds(userInput.fnpSubRecPair)

        # For the purpose of matching demw and new reclassif
        # sub nos, the dict is processed to a new format
        # with nested dict: ws_key1, subdemw_key2:subrecno_value.
        self.wssubflddict2 = self.modifywssubdict(
                self.wssubflddict)

        # Read in asc data for later processing
        self.dtsubno = gdalfuncs.readASCstr(userInput.fnpSubWsAsc)

        
        self.dtslp = gdalfuncs.readASCfloat(userInput.fnpSd8Asc)
        self.dtplen = gdalfuncs.readASCfloat(userInput.fnpPlenAsc)
        self.dtsol = gdalfuncs.readASCstr(userInput.fnpWsExtSolAsc)
        self.dtlu = gdalfuncs.readASCstr(userInput.fnpWsExtLuAsc)
        self.dtstrmasc = gdalfuncs.readASCstr(userInput.fnpSrcStreamAsc)
        self.dtelev = gdalfuncs.readASCfloat(userInput.fnpDemASC)

        ## Create Pandas dataframe to store all asc data
        self.dfasc = pd.DataFrame(self.dtsubno[3],
                                  columns=['subno'])

        self.dfasc['slope'] = self.dtslp[3]
        self.dfasc['plen'] = self.dtplen[3]
        self.dfasc['soilid'] = self.dtsol[3]
        self.dfasc['luid'] = self.dtlu[3]
        self.dfasc['strm01'] = self.dtstrmasc[3]
        self.dfasc['elev'] = self.dtelev[3]

        self.uniqluno = self.dfasc['luid'].unique()

        ## Start processing the dataframe for various variables
        ## Subarea no
        # 1. Delete rows where subarea are nodata:
        #     This will reduce the processing time.
        self.dfasc = self.dfasc.drop(self.dfasc[
                self.dfasc.subno == self.dtsubno[2]].index)

        self.uniqsubno = self.dfasc['subno'].unique()

        # In order to remove the potential problems of having
        # to simulate water, I will need to remove those land
        # uses that are water.
        self.waterlus = list(map(str, [50,60,70,100]))
        self.nodatalus = list(map(str, [0,81,88]))
        # ~ turn True to False
        # This may cause some issue where water are a lot.
        # I will add another calculation to get the percent
        # of water area, which will be treated as ponds.
        #self.dfasc = self.dfasc[
            #~self.dfasc['luid'].isin(self.waterlus)]

        # Get the stream attribute information
        ## Stream attributes
        # The attritube table from the stream.shp.
        # This will privide channel length, channel slope,
        # and other useful information
        self.strmAtt = gdalfuncs.getShpAttributes(userInput.fnpStreamShp)

        # treedict: a dictionary storing the connection among
        # different subareas, including downstream, upstream,
        # stream order, etc.
        self.treedict = graphUtil.readTree(userInput.fnpTree)

        # Either the streamAtt or the tree file has some problem
        # of having numbers that does not exist in the demw.
        # All the attributes of subareas area processed using
        # stream number in the demw file. So, I need to process
        # the missing numbers in demw but existing in streamAtt
        # or tree file.
        self.treedict2 = graphUtil.rmExtraStrm(self.uniqsubno,
                                         self.treedict)

        # A graph representing the subareas
        self.watershedGraph = graphUtil.graphForWS(
            self.treedict2)

        self.uniqsoils = self.dfasc['soilid'].unique()
        if ("0" in self.uniqsoils):
            # Find the most frequent soil ids in the soil list(This should not be 0)
            self.mostsoilid = self.dfasc['soilid'].value_counts().idxmax()
            if (self.mostsoilid == '0'):
                self.mostsoilid = "12"
            # Create an np array to be added in the pandas to replace the 0s
            # with the most soil id
            self.mostsoilarray = np.array([self.mostsoilid] * len(self.dfasc[self.dfasc['soilid'] == '0']))
            # Modify
            self.dfasc.loc[self.dfasc['soilid'] == '0', "soilid"] = self.mostsoilarray

        # Deal with land use
        # If there is water or other unwanted land use
        # Mocify the 0 values or water to the most frequent values in
        # landuse
        # 1. Get unique values of the soil list
        self.uniqlus = self.dfasc['luid'].unique()
        for luuid in self.uniqlus:
            if (luuid in self.waterlus):
                # Find the most frequent soil ids in the soil list(This should not be 0)
                self.mostluid = self.dfasc['luid'].value_counts().idxmax()
                if self.mostluid in self.waterlus:
                    self.mostluid = "10"
                # Create an np array to be added in the pandas to replace the 0s
                # with the most soil id
                self.mostluarray = np.array([self.mostluid] * len(self.dfasc[self.dfasc['luid'] == luuid]))
                # Modify
                self.dfasc.loc[self.dfasc['luid'] == luuid, "luid"] = self.mostluarray

        # based on the intended scenario, the lu column will be modified to the
        # intended scenario
        self.mostluarray = np.array([self.mostluid] * len(self.dfasc[self.dfasc['luid'] == luuid])) 

        # Add a slopeGroup For processing
        self.dfasc['slopeGroup'] = self.dfasc['slope'].apply(
                                        self.getslopeIndex)

        # Generate CropSoilSlopeNumber
        self.dfasc['subCropSoilSlope'] = self.dfasc.apply(
                                        self.addCropSoilSlope,
                                        axis=1)

        # Calculate average dem/elevation for the subarea
        self.avgElev = self.dfasc.groupby('subno')[
                'elev'].mean().to_dict()

        # Recording the apperance of each combination of crop, soil
        # slope at each subarea
        # Count appearances of each combination for all subareas
        self.subCSSCounts = self.dfasc[
                'subCropSoilSlope'].value_counts()

        # Here we used the major combination of slope, soil, landuse
        # (nass) combination for determining subareas
        # The subCSSCounts is a series. We would like to process it to
        # a dataframe and then processing to get the combination
        # in a subarea with the maximum area
        self.subCSSCountsMax = self.subCSSCounts.to_frame()

        self.subCSSCountsMax['comb'] = self.subCSSCountsMax.index
        # Break the combination to list to add new columns on that.
        self.subCSSCountsMax['comblst'] = self.subCSSCountsMax.apply(
                                self.breakCSSComb,
                                axis=1)
        self.subCSSCountsMax['subno'] = self.subCSSCountsMax.apply(
                                self.assignSub,
                                axis=1)

        self.subCSSCountsMax['lu'] = self.subCSSCountsMax.apply(
                                self.assignLu,
                                axis=1)

        # Get the max combination for each subarea
        self.subCSSMaxDict, self.pondfrac = self.getCSSComb(
                self.subCSSCountsMax,
                self.waterlus)

        # Count appearances of each subarea no to get the subarea areas
        self.subareaArea = self.dfasc['subno'].value_counts().to_dict()

        ## Average upland slope
        # this is the average of slopes for all grids
        # Calculate average slope of each subarea
        self.avgSlope = self.dfasc.groupby('subno')['slope'].mean().to_dict()
        #print(self.avgSlope)
        ## Average upland slopelength:
        # This is calculated as the average of flowpath length
        # from the plen file (results of gridnet)
        # This value may need to be updated later. The method
        # to calculate it needs further exploration
        self.avgSlpLen = self.dfasc[['subno', 'plen']].groupby('subno')['plen'].mean().to_dict()

        ## Subarea Centroid
        # The latitude and longitude values for the
        # centroids of each subarea.
        self.subLatLong = gdalfuncs.getCentroid(userInput.fnpSubWsShp)
        #print(self.subLatLong)
        # Land use number manning N and management options
        self.nassLuMgtUpn = self.readCSVtoDict(userInput.tblumgtupn)
        # Channel manning N
        self.channelManN = self.readChMnTb(userInput.tbchn)
        ## Subarea areas
        self.cellsize = float(self.dtsubno[4])

        ## Channel length:
        # Channel length is the length from the subarea outlet to
        # the most distant point. We have P len.
        # If the subarea is an extreme subarea, channel length is the
        # maximum plen value for all channel cells.
        # If the subarea is an routing subarea, channel length need to be
        # larger than reach length. It will be the reach length + the maximum plen.
        # for non channel area.
        # self.channenLen: maximum plen for channel
#        self.channenLen = self.dfasc[self.dfasc['strm01'] == '1'  \
#                ][['subno', 'plen']].groupby('subno')['plen'].max().to_dict()

        # This channel length has a problem and I will
        # update to use the value from the channel.
        # Since the non existing stream has been removed,
        # I can use it directly.
        # Another thing to pay attention is the 0 values,
        # SWAT may take it but for downstream, channel can
        # not equal to slope length. I will process later.
        self.rchchannenLen = self.getrchChannelLen(self.strmAtt)
        self.channenLen = self.dfasc[self.dfasc['strm01'] == '1'  \
                ][['subno', 'plen']].groupby('subno')['plen'].max().to_dict()





    def modifywssubdict(self, wssubflddict):

        wsdict2 = copy.deepcopy(wssubflddict)
        for key, value in wssubflddict.items():
            wsdict2[key] = {}
            for vidx in range(len(value[0])):
                #print(wsdict2[key][0][vidx])
                wsdict2[key][value[0][vidx]] = value[1][vidx]

        return wsdict2


    def readWsSubFlds(self, fn_json):

        inf_usrjson = {}
        with open(fn_json) as json_file:
            inf_usrjson = json.loads(json_file.read())

        return inf_usrjson



    def getCSSComb(self, df, waterlus):

        '''
        Add Get the maximum combination for each subarea
        '''
        outdict = {}
        pondpercent = {}

        subNos = df['subno'].unique()

        for sid in subNos:

            dftemp = 0
            dftemp = df[df['subno'] == sid]

            dftemp = dftemp[dftemp[
                    'subCropSoilSlope']==dftemp[
                            'subCropSoilSlope'].max()]

            outdict[int(sid)] = dftemp.index[0].split('_')

            totalarea = 0
            totalarea = dftemp['subCropSoilSlope'].sum()

            # Count the counts of water land uses
            dfwstmp = dftemp[dftemp['lu'].isin(waterlus)]

            pondarea = 0
            pondarea = dfwstmp['subCropSoilSlope'].sum()

            pondpercent[int(sid)] = pondarea/totalarea



        return outdict, pondpercent


    def breakCSSComb(self, df):

        '''
        Add one column of combination of subarea no, crop/landuse, soil,
        and slopeGroup
        '''
        cropSoilSlope = df['comb'].split('_')

        return cropSoilSlope


    def assignSub(self, df):

        '''
        Add one column of combination of subarea no, crop/landuse, soil,
        and slopeGroup
        '''
        subno = df['comblst'][0]

        return subno


    def assignLu(self, df):

        '''
        Add one column of combination of subarea no, crop/landuse, soil,
        and slopeGroup
        '''
        lu = df['comblst'][1]

        return lu



    def addCropSoilSlope(self, df):

        '''
        Add one column of combination of subarea no, crop/landuse, soil,
        and slopeGroup
        '''
        cropSoilSlope = '%s_%s_%s_%i' %(df['subno'],
                                     df['luid'],
                                     df['soilid'],
                                     df['slopeGroup'])

        return cropSoilSlope


    def getslopeIndex(self, slopePercent):

        '''
        slopePercent: slope value in asc is value, percent should
        time 100.
        '''
        n = len(self.slopeGroup)
        for index in range(n):
            if slopePercent*100 < self.slopeGroup[index]:
                return index
        return n


    def readJSON(self, fn_json):

        inf_usrjson = {}

        with open(fn_json) as json_file:
            inf_usrjson = json.loads(json_file.read())
        #pprint.pprint(inf_usrjson)
        json_file.close()

        return inf_usrjson




    def readChMnTb(self, fintable):
        '''
        Read the table containing manning N for channels
        with different conditions.

        fintable: path of the file.
        It is a text file with the manning n for different conditions.

        The table cantains complete information for determining
        channel manning N.
        Here the Earth will be used as default. The inclusion
        of this table will further assist simulation of
        channel erosion.
        '''

        fid = open(fintable, 'r')
        lif = fid.readlines()
        fid.close()

        for idx in range(len(lif)):
            lif[idx] = lif[idx].split(',')

        return lif




    def readCSVtoDict(self, finCSV):
        '''
        Use to read the fin_nassmgtupn table.
        This table contains information for nass value, and
        the following columns.
        Term definition:
        #Group: the group of the crop for better sorting.
        #APEXMGT: the name of the OPS files that will be used
        to simulate the tillage management. This can be updated
        later for more detailed control.
        #LUNOCV: land use no for curve number value determination.
        This was determined based on the land use table of the
        apex user manual 1501. For most crops, I will use the
        straight poor as default, which is the first one.
        This can be refined later.
        UPN: the upland manning's N number. I will use the
        conventional tillage residue as default value.

        The output of this function will return a dictionary
        with NASSvalue as keys since we have this from land use.
        Then LUNO and UPN can be determined.

        Columnnames:

        '0NASSValue',
        '1CropName', '2Group', '3APEXMGT', '4APEXMGTNO',
        '5LUNOCV_Straight_Poor', '6LUNOCV_Straight_Good',
        '7LUNOCV_Contoured_Poor', '8LUNOCV_Contoured_Good',
        '9LUNOCV_ContouredTerraced_Poor',
        '10LUNOCV_ContouredTerrace_Good',
        '11UPN_Conventional_Tillage_No_Residue',
        '12UPN_Conventional_Tillage_Residue',
        '13UPN_Chisel_Plow_No_Residue',
        '14UPN_Chisel_Plow_Residue',
        '15UPN_Fall_Disking_Residue',
        '16UPN_No_Till_No_Residue',
        '17UPN_No_Till_With_Residue_0to1ton',
        '18UPN_No_Till_With_Residue_2to9ton'
        '''

        import csv

        #columnname = []
        values = []
        outdict = {}

        with open(finCSV) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    #columnname = row
                    line_count += 1
                else:
                    values.append(row)
                    line_count += 1

        for vid in values:
            outdict[vid[0]] = vid

        return outdict



    def getrchChannelLen(self, strmshpatt):

        channellen = {}
        for k, v in strmshpatt.items():
            channellen[k] = float(v[6])

        return channellen







