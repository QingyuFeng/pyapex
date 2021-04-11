# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import json, copy

from .gdalfuncs import gdalfuncs
from .graphUtil import graphUtil

gdalfuncs = gdalfuncs()
graphUtil = graphUtil()


class ascInfoWSOlt():
    def __init__(self, defaultFNFD):
        """Constructor."""

        # Read in asc data for later processing
        self.dtsubno = gdalfuncs.readASCstr(defaultFNFD.fnpSubWsAsc)
        self.dtslp = gdalfuncs.readASCfloat(defaultFNFD.fnpSd8Asc)
        self.dtplen = gdalfuncs.readASCfloat(defaultFNFD.fnpPlenAsc)
        self.dtsol = gdalfuncs.readASCstr(defaultFNFD.fnpWsExtSolAsc)
        self.dtlu = gdalfuncs.readASCstr(defaultFNFD.fnpWsExtLuAsc)
        self.dtstrmasc = gdalfuncs.readASCstr(defaultFNFD.fnpSrcStreamAsc)
        self.dtelev = gdalfuncs.readASCfloat(defaultFNFD.fnpDemASC)

        # Slope group to be modified. Included here for
        # Future reference
        self.slopeGroup = defaultFNFD.usrslpgroup

        ## Create Pandas dataframe to store all asc data
        self.dfasc = pd.DataFrame(self.dtsubno[3],
                                  columns=['subno'])

        self.dfasc['slope'] = self.dtslp[3]
        self.dfasc['plen'] = self.dtplen[3]
        self.dfasc['soilid'] = self.dtsol[3]
        self.dfasc['luid'] = self.dtlu[3]
        self.dfasc['strm01'] = self.dtstrmasc[3] 
        self.dfasc['elev'] = self.dtelev[3]

        ## Start processing the dataframe for various variables
        ## Subarea no
        # This might not be used. Keep it commented.
        # 1. Delete rows where subarea are nodata:
        #     This will reduce the processing time.
        self.dfasc = self.dfasc.drop(self.dfasc[
                self.dfasc.subno == self.dtsubno[2]].index)

        self.uniqsubno = self.dfasc['subno'].unique()
                
        # Stream routing orders
        ## Stores the order of subareas. This will
        ## serve as the first line of each subarea in the .sub
        ## file, starting with an extreme and flow to 
        ## the outlet of the watershed.

        # Get the stream attribute information
        ## Stream attributes
        # The attritube table from the stream.shp.
        # This will privide channel length, channel slope,
        # and other useful information
        self.strmAtt = gdalfuncs.getShpAttributes(defaultFNFD.fnpStreamShp)

        # treedict: a dictionary storing the connection among
        # different subareas, including downstream, upstream,
        # stream order, etc.
        self.treedict = graphUtil.readTree(defaultFNFD.fnpTree)
        
        # Either the streamAtt or the tree file has some problem
        # of having numbers that does not exist in the demw.
        # All the attributes of subareas area processed using
        # stream number in the demw file. So, I need to process
        # the missing numbers in demw but existing in streamAtt
        # or tree file. 
        self.treedict2 = graphUtil.rmExtraStrm(self.uniqsubno,
                                         self.treedict)
        
        ## Outlet and watershed graph are the input for the
        ## dfs_recursive function
        ## Outlet of the watershed: identified by getting the stream
        ## number, whose downstream is -1
        self.outletStrNo = [k for k,v in self.strmAtt.items() if v[1]=='-1'][0]
        ## Representing watershed in Graph format:
        ## basically a dictionary: wsGraph = {streamNo: [neighbour1, nb2]}
        
        self.watershedGraph = graphUtil.graphForWS(
                                self.treedict2)
        ## self.subRouting: a list contains the minus values
        ## when the area of the subarea need to be minus in apex
        ## sub file.

        #print('graph', self.watershedGraph)
        
        self.subRouting = []
        ## self.subPurePath: a list contains the routing path
        ## of the subareas. This was included because the strmAtt
        ## is a dictionary with positive keys. 
        self.subPurePath = []
        self.subPurePath, self.subRouting = self.dfs_iterative(
                                    self.watershedGraph,
                                    self.outletStrNo)
        # Add a slopeGroup For processing
        self.dfasc['slopeGroup'] = self.dfasc['slope'].apply(
                                        self.getslopeIndex)
        
        # In order to remove the potential problems of having
        # to simulate water, I will need to remove those land
        # uses that are water.
        self.waterlus = map(str, [50,60,70,100])
        # ~ turn True to False
        #self.dfasc = self.dfasc[~self.dfasc['luid'].isin(self.waterlus)]
       
        # Deal with the 0 values in soil and land use
#        print(self.dfasc['soilid'].value_counts().idxmax())
#        print(self.dfasc['luid'].value_counts().idxmax())
#        print(self.dfasc['slope'].value_counts().idxmax())

        # Mocify the 0 values or water to the most frequent values in
        # soil
        # 1. Get unique values of the soil list
        self.uniqsoils = self.dfasc['soilid'].unique()

        if ("0" in self.uniqsoils):
            # Find the most frequent soil ids in the soil list(This should
            # not be 0)
            self.mostsoilid = self.dfasc['soilid'].value_counts().idxmax()
            if (self.mostsoilid == '0') or (self.mostsoilid == '1'):    
                self.mostsoilid = "4233"
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
#                print(len(self.dfasc[self.dfasc['luid'] == luuid]))
                # Find the most frequent soil ids in the soil list(This should
                # not be 0)
                self.mostluid = self.dfasc['luid'].value_counts().idxmax()
                if self.mostluid in self.waterlus:
                    self.mostluid = "90"
                # Create an np array to be added in the pandas to replace the 0s
                # with the most soil id
                self.mostluarray = np.array([self.mostluid] * len(self.dfasc[self.dfasc['luid'] == luuid]))
                # Modify
                self.dfasc.loc[self.dfasc['luid'] == luuid, "luid"] = self.mostluarray

        # Generate CropSoilSlopeNumber
        self.dfasc['subCropSoilSlope'] = self.dfasc.apply(
                                        self.addCropSoilSlope,
                                        axis=1)

        # Calculate average dem/elevation for the subarea
        self.avgElev = self.dfasc.groupby('subno')['elev'].mean().to_dict()

        ## Processing subarea information
        # Recording the apperance of each combination of crop, soil
        # slope at each subarea
        # Count appearances of each combination for all subareas
        self.subCSSCounts = self.dfasc['subCropSoilSlope'].value_counts()

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
        # Get the max combination for each subarea
        self.subCSSMaxDict = self.getCSSComb(self.subCSSCountsMax)
        #print(self.subCSSMaxDict)
        
        ## Subarea areas
        self.cellsize = float(self.dtsubno[4])
        # Count appearances of each subarea no to get the subarea areas
        self.subareaArea = self.dfasc['subno'].value_counts().to_dict()

        ## Average upland slope
        # this is the average of slopes for all grids
        # Calculate average slope of each subarea
        self.avgSlope = self.dfasc.groupby('subno')['slope'].mean().to_dict()
        ## Average upland slopelength:
        # This is calculated as the average of flowpath length
        # from the plen file (results of gridnet)
        # This value may need to be updated later. The method
        # to calculate it needs further exploration
#        self.avgSlpLen = self.dfasc[self.dfasc['strm01'] == '0'  \
#                ][['subno', 'plen']].groupby('subno')['plen'].mean().to_dict()

        # self.avgSlpLen = self.dfasc[['subno', 'plen']].groupby('subno')['plen'].mean().to_dict()
        self.avgSlpLen = self.getAvgSlpBasin(self.avgSlope)
        ## Subarea Centroid
        # The latitude and longitude values for the
        # centroids of each subarea.
        self.subLatLong = gdalfuncs.getCentroid(defaultFNFD.fnpSubWsShp)
        # Land use number manning N and management options
        self.nassLuMgtUpn = self.readCSVtoDict(defaultFNFD.tblumgtupn)
        # Channel manning N
        self.channelManN = self.readChMnTb(defaultFNFD.tbchn)
        
        # A dictionary to store the ws_subno, soil, landuse,
        # latitude, longitude. The ws_subno will be the order
        # number of the list in soil, management, and daily weather
        # station.
        self.wsSubSolOpsLatLon = {}

        ## Channel length:
        # Channel length is the length from the subarea outlet to
        # the most distant point. We have P len.
        # If the subarea is an extreme subarea, channel length is the
        # maximum plen value for all channel cells. 
        # If the subarea is an routing subarea, channel length need to be
        # larger than reach length. It will be the reach length + the maximum plen.
        # for non channel area.
        # self.channenLen: maximum plen for channel

        self.rchchannenLen = self.getrchChannelLen(self.strmAtt)
        self.channenLen = self.dfasc[self.dfasc['strm01'] == '1'  \
                ][['subno', 'plen']].groupby('subno')['plen'].max().to_dict()
        
        


    def getAvgSlpBasin(self, avgSlpDict):
        """
        This function is copied and modified from QSWAT plus.
        This is the way how slope lenth is determined.
        Estimate the average slope length in metres from the mean slope.
        
        """     
        sloplendict = {}
        for key, value in avgSlpDict.items():
            if value < 0.01: 
                sloplendict[key] = 120
            elif value < 0.02: 
                sloplendict[key] = 100
            elif value < 0.03: 
                sloplendict[key] = 90
            elif value < 0.05: 
                sloplendict[key] = 60
            else: 
                sloplendict[key] = 30

        return sloplendict



    def getrchChannelLen(self, strmshpatt):
        
        channellen = {}
        for k, v in strmshpatt.items():
            channellen[k] = float(v[6])
            
        return channellen
                    
        
    
    def modifywssubdict(self, wssubflddict):
        
        wsdict2 = copy.deepcopy(wssubflddict)
        
        for key, value in wssubflddict.items():
            wsdict2[key] = {}
            for vidx in range(len(value[0])):
                #print(wsdict2[key][0][vidx])
                wsdict2[key][value[0][vidx]] = value[1][vidx]

        return wsdict2
                
            

    def readWsSubnos(self, fn_json):

        inf_usrjson = {}
        
        with open(fn_json) as json_file:    
            inf_usrjson = json.loads(json_file.read())
        #pprint.pprint(inf_usrjson)
        json_file.close()
        
        return inf_usrjson

    


    def dfs_iterative(self, graph, start):
        stack, path, pathminus = [start], [], []

        # Stack as the starting point
        while stack:
            # Signed vertex: for path routing
            signedvertex = stack.pop()
            # remove sign for looping
            vertex = str(abs(int(signedvertex)))
            # Mark vertex as visited.
            if vertex in path:
                continue
            # If not visited, append it.
            path.append(vertex)
            pathminus.append(signedvertex)

            for nbid in range(len(graph[vertex])):
                if nbid > 0:
                    neighbor = '-%s' %(graph[vertex][nbid])
                else:
                    neighbor = graph[vertex][nbid]
                    
                stack.append(neighbor)

        return path, pathminus







    def getCSSComb(self, df):

        '''
        Add Get the maximum combination for each subarea
        '''
        outdict = {}

        subNos = df['subno'].unique()

        for sid in subNos:

            dftemp = 0
            dftemp = df[df['subno'] == sid]
            #.groupby('comb')['subCropSoilSlope'].max()
            dftemp = dftemp[dftemp['subCropSoilSlope']==dftemp['subCropSoilSlope'].max()]

            outdict[int(sid)] = dftemp.index[0].split('_')
        
        return outdict


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

        columnname = []
        values = []
        outdict = {}
        
        with open(finCSV) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    columnname = row
                    line_count += 1
                else:
                    values.append(row)
                    line_count += 1
                    
        for vid in values:
            outdict[vid[0]] = vid
        
        return outdict




    def readASCfloat(self, finasc):

        # Store data into a list
        data = []
        
        # Reading files to a list 

        with open(finasc, 'r') as f:
            lif = f.read().splitlines()

        # The file some times contain wrong lines.
        # TODO: check whether the value rows are the same
        # The demws.asc for dem/elevation has one more row


        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split(' ')
            while '' in lif[lidx]:
                lif[lidx].remove('')

            if lidx > 5:              
                lif[lidx] = list(map(float, lif[lidx]))
        # 0: ncols, 1: nrows, 5: NoDATA, 4: cellsize
        data.append(lif[0][1])
        data.append(lif[1][1])    
        data.append(lif[5][1])
        
        #print(lif[:4])
        del(lif[:7])
        del(lif[-1])

        data.append(lif)

        # Convert 2d asc array into 1d array
        data[3] = np.asarray(data[3]).ravel()
        #print(data[3].shape)

        return data


            
    def dfs_recursive(self, graph, vertex, path=[], pathminus=[]):
        '''
        Using Depth first search algorithm to find the routing schemes
        Basic idea is:
        1. Represent the watershed connection in graphs. Using the function above.
        2. Starting from the root(outlet of the subarea), find all its neighbours.
        For each of the neighbour, of the first step, find all its upstreams. For
        each upstream, find the upstreams using the same function, until the very
        end of the branch. Then, come back for the second upstream, and repeat.
        3. At each level, append the visited path into a list, if it is not visited,
        go search, if visited (marked by not in), skip.
        May be not well explained, but it worked now, I will come back to provide
        better understanding. (TODO).

        to call the function:
        graph: graph representation of the watershed.
        vertex: start with the outlet.
        '''
        absvertex = str(abs(int(vertex)))
        
        path += [absvertex]
        
        pathminus += [vertex]
        
        for nbid in range(len(graph[absvertex])):
            neighbor = graph[absvertex][nbid]
            
            if neighbor not in path:
                if nbid > 0:
                    neighbor = '-%s' %(neighbor)
                path, pathminus = self.dfs_recursive(graph, neighbor, path, pathminus)

        return path, pathminus




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
        
        
    def addCSSCounts(self, subCSSComb):
        '''
        Add a column count the appearance for each combination of
        crop, soil, slopeGroup in each subarea
        '''
        
        return self.subCSSCounts[subCSSComb]
        
    def addsubArea(self, subno):
        '''
        Add a column count the appearance for each combination of
        crop, soil, slopeGroup in each subarea
        '''
        return self.subareaArea[subno]







        