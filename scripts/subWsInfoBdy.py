# -*- coding: utf-8 -*-
import copy

class subWsInfo():

    def __init__(self, wsidx, ascInfoBdy):

        """Constructor."""
        self.WsSubInfoReset()

        # A dataframe containing only information for the watershed
        # being processing.
        # Getting the subarea nos of this watershed.
        self.Subnos = None
        self.Subnos = ascInfoBdy.wssubflddict[wsidx][0]
#        print("Hi here:  ", self.Subnos)
        # Removing unneeded information in the subarea
        # wsSubInfoDf: dataframe containing only subareas of the
        # watershed being processing.
        self.InfoDf = None
        self.InfoDf = copy.deepcopy(ascInfoBdy.dfasc[
            ascInfoBdy.dfasc['subno'].isin(self.Subnos)])#.copy()

        # In order to use the dfs algorithm, here, we need to
        # figure out which is the outlet subarea. These watershed
        # was generated using depth first search. The first one
        # is the outlet subarea.
        self.wsOutlet = None
        self.wsOutlet = self.Subnos[0]

        # Getting the routing and pure paths
        ## self.subRouting: a list contains the minus values
        ## when the area of the subarea need to be minus in apex
        ## sub file.

        ## self.subPurePath: a list contains the routing path
        ## of the subareas. This was included because the strmAtt
        ## is a dictionary with positive keys.
        self.subRouting = []
        self.subPurePath = []
        self.subPurePath, self.subRouting = self.dfs_iterative(
                                    ascInfoBdy.watershedGraph,
                                    self.wsOutlet)


    def WsSubInfoReset(self):
        self.Subnos = 0
        self.InfoDf = 0
        self.wsGraph = {}
        self.wsOutlet = 0
        self.subRouting = []
        self.subPurePath = []



    def modifywsJSON(self,
                     wsidx,
                     sWVJSON,
                     wsSubCtr,
                     wssubsolopslatlong,
                     subPurePath,
                     subRouting,
                     ascInfoBdy
                     ):
        wsjsonkey2 = None
        wsjsonkey2 = 'watershed%i' %(wsidx+1)
        # Reset all variables to prevent continuous
        sWVJSON[wsjsonkey2]['model_setup']['subid_snum'] = []
        sWVJSON[wsjsonkey2]['model_setup'][
                'description_title'] = []
        sWVJSON[wsjsonkey2]['geographic']['latitude_xct'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['longitude_yct'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['avg_upland_slp'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['avg_upland_slplen_splg'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['uplandmanningn_upn'
                ] = []
        sWVJSON[wsjsonkey2]['soil']['soilid'] = []
        sWVJSON[wsjsonkey2]['management']['opeartionid_iops'
                ] = []
        sWVJSON[wsjsonkey2]['management']['OPSName_Reference'
                ] = []
        sWVJSON[wsjsonkey2]['land_use_type']['land_useid_luns'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['channelslope_chs'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['reach_slope_rchs'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['channelmanningn_chn'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['channellength_chl'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['reach_length_rchl'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['wsa_ha'
                ] = []
        sWVJSON[wsjsonkey2]['geographic']['subarea_elev_sael'
                ] = []
#        sWVJSON[wsjsonkey2]['pond']['frac_pond_pcof'
#                ] = []
        sWVJSON[wsjsonkey2]['drainage']['drainage_depth_idr'
                ] = []

        subPath = []
        subPathSign = []
        for sidx in subPurePath[::-1]:
            subPath.append(sidx)
        for sidx2 in subPurePath[::-1]:
            subPathSign.append(sidx2)

        for subid in range(len(subPath)):
            # Updating the counter
            wsSubCtr = wsSubCtr + 1
            wssubsolopslatlong[wsSubCtr] = {}
            # Add the subarea to the sWVJSON
            subNo = 0
            subNo = int(subPath[subid])
            # Append ws sub no to the dictionary
            wssubsolopslatlong[wsSubCtr]['wsno'] = wsidx
            wssubsolopslatlong[wsSubCtr]['subno'] = subNo

            # Updating the counter
            # subNorecal: is the original number from
            # taudem delineation. It is used in the tree
            # for routing. And here we can safely use
            # new numbers?
            subNorecal = ascInfoBdy.wssubflddict2[
                    str(wsidx+1)][str(subNo)]
            wssubsolopslatlong[wsSubCtr]['subNorecal'] = subNorecal

            #print(subid, subNo)
            # Subarea information are stored in lists
            # Update subarea NO: for routing
            sWVJSON[wsjsonkey2]['model_setup'][
                'subid_snum'].append(subNorecal)

            # Update description line:
            sWVJSON[wsjsonkey2]['model_setup'][
                'description_title'].append(subid+1)

            # Updating Latitude and longitude
            sWVJSON[wsjsonkey2]['geographic']['latitude_xct'
                ].append(ascInfoBdy.subLatLong[subNo][0])
            sWVJSON[wsjsonkey2]['geographic']['longitude_yct'
                ].append(ascInfoBdy.subLatLong[subNo][1])
            sWVJSON[wsjsonkey2]['geographic']['subarea_elev_sael'
                ].append(ascInfoBdy.avgElev[str(subNo)])


            # Append iops no to the dictionary
            wssubsolopslatlong[wsSubCtr]['lat'] = ascInfoBdy.subLatLong[subNo][0]
            wssubsolopslatlong[wsSubCtr]['lon'] = ascInfoBdy.subLatLong[subNo][1]

            # Updating Average upland slope
            sWVJSON[wsjsonkey2]['geographic']['avg_upland_slp'
                ].append(ascInfoBdy.avgSlope[str(subNo)])

            slplen = 0.0
            slplen = ascInfoBdy.avgSlpLen[str(subNo)]

            if (slplen > 80.0):
                # Updating Average upland slope length
                sWVJSON[wsjsonkey2]['geographic']['avg_upland_slplen_splg'
                    ].append(80.0)
            elif( (slplen > 0.0) and (slplen <= 80.0)):
                sWVJSON[wsjsonkey2]['geographic']['avg_upland_slplen_splg'
                    ].append(slplen)
            else:
                # Updating Average upland slope length
                sWVJSON[wsjsonkey2]['geographic']['avg_upland_slplen_splg'
                    ].append(5.0)

            # Updating Manning N upland
            # tempCSS: temp list storing the crop soil slope
            # combination [sub, nass lu, soil mukey, slop group]
            tempCSS = []
            tempCSS = ascInfoBdy.subCSSMaxDict[subNo]
            sWVJSON[wsjsonkey2]['geographic']['uplandmanningn_upn'
                ].append(ascInfoBdy.nassLuMgtUpn[tempCSS[1]][12])

            # Updating soil id
            #sWVJSON['soil']['soilid'].append(tempCSS[2])
            sWVJSON[wsjsonkey2]['soil']['soilid'].append(wsSubCtr)
            # Append soil no to the dictionary
            wssubsolopslatlong[wsSubCtr]['mukey'] = tempCSS[2]

            # Update IOPS NO
            #sWVJSON['management']['opeartionid_iops'
                #].append(ascInfoBdy.nassLuMgtUpn[tempCSS[1]][4])
            sWVJSON[wsjsonkey2]['management']['opeartionid_iops'
                ].append(wsSubCtr)
            sWVJSON[wsjsonkey2]['management']['OPSName_Reference'
                ].append(ascInfoBdy.nassLuMgtUpn[tempCSS[1]][3])

            # Append iops no to the dictionary
            wssubsolopslatlong[wsSubCtr]['iopsno'] = ascInfoBdy.nassLuMgtUpn[tempCSS[1]][4]
            wssubsolopslatlong[wsSubCtr]['iopsnm'] = ascInfoBdy.nassLuMgtUpn[tempCSS[1]][3]

            # Updating land use no
            # There are other conditions, we will use the first
            # as default. TODO: may need to refine this later.
            sWVJSON[wsjsonkey2]['land_use_type']['land_useid_luns'
                ].append(ascInfoBdy.nassLuMgtUpn[tempCSS[1]][5])

            # Updating Channel slope:TODO: Calculate the channel and
            # Reach slope later some how
            #print(GetSubInfo.strmAtt[subNo][10])
            sWVJSON[wsjsonkey2]['geographic']['channelslope_chs'
                ].append(ascInfoBdy.strmAtt[str(subNo)][10])

            # Updating Reach slope:
            sWVJSON[wsjsonkey2]['geographic']['reach_slope_rchs'
                ].append(ascInfoBdy.strmAtt[str(subNo)][10])

            # Updating Channel manning n
            sWVJSON[wsjsonkey2]['geographic']['channelmanningn_chn'
                ].append(ascInfoBdy.channelManN[0][4])

            subarea_area = 0.0
            subarea_area = ascInfoBdy.subareaArea[str(subNo)]*ascInfoBdy.cellsize*ascInfoBdy.cellsize/10000.0
            rchchllen = 0.0
            chllen = 0.0
            rchchllen = ascInfoBdy.rchchannenLen[str(subNo)]/1000.0
            chllen = ascInfoBdy.channenLen[str(subNo)]/1000.0

            # make sure we have value not 0, had a minimum of 30 m
            if (rchchllen < 0.03):
                rchchllen = 0.03
            if (chllen < 0.03):
                chllen = 0.03
            if (rchchllen > chllen):
                chllen = rchchllen + 0.01
#            print("reach, channel", rchchllen, chllen)
            if (subarea_area < 20):
                if ((ascInfoBdy.strmAtt[str(subNo)][2] == '-1')
                    and (ascInfoBdy.strmAtt[str(subNo)][3] == '-1')):
                    sWVJSON[wsjsonkey2]['geographic']['channellength_chl'].append(0.5)
                    sWVJSON[wsjsonkey2]['geographic']['reach_length_rchl'].append(0.5)
                # If it is a routing watershed, channel length is the reach len
                # + max channel TODO: will be modified to get the channel length
                # for the watershed outlet
                else:
                    sWVJSON[wsjsonkey2]['geographic']['channellength_chl'
                       ].append(0.8)
                    sWVJSON[wsjsonkey2]['geographic']['reach_length_rchl'
                         ].append(0.5)
            else:
                # -1 means a downstream subarea
                if ((ascInfoBdy.strmAtt[str(subNo)][2] == '-1')
                    and (ascInfoBdy.strmAtt[str(subNo)][3] == '-1')):
                    sWVJSON[wsjsonkey2]['geographic']['channellength_chl'
                        ].append(rchchllen)
                    sWVJSON[wsjsonkey2]['geographic']['reach_length_rchl'
                        ].append(rchchllen)
                                                                                                                                                                                             # If it is a routing watershed, channel length is the reach len
                # + max channel TODO: will be modified to get the channel length
                # for the watershed outlet
                else:
                    sWVJSON[wsjsonkey2]['geographic']['channellength_chl'
                        ].append(chllen)
                    sWVJSON[wsjsonkey2]['geographic']['reach_length_rchl'
                         ].append(rchchllen)

            # Updating Watershed area:
            #print(float(GetSubInfo.subareaArea[str(subNo)])*GetSubInfo.cellsize/10000.0)
            # The area for adding should be minus
            if '-' in self.subRouting[subid]:
                sWVJSON[wsjsonkey2]['geographic']['wsa_ha'
                    ].append('-%.5f' %(ascInfoBdy.subareaArea[str(subNo)]
                         *ascInfoBdy.cellsize*ascInfoBdy.cellsize/10000.0))
            else:
                sWVJSON[wsjsonkey2]['geographic']['wsa_ha'
                ].append('%.5f' %(ascInfoBdy.subareaArea[str(subNo)]
                         *ascInfoBdy.cellsize*ascInfoBdy.cellsize/10000.0))

            # At this time, tile drainage is sitll unknow, but need to be
            # initiated.
            sWVJSON[wsjsonkey2]['drainage']['drainage_depth_idr'
                ].append('0')

        return wsSubCtr, wssubsolopslatlong


    def dfs_iterative(self, graph, start):
        '''
        Using iterative pathways to find the routes.
        This algorithm used the stack data structure.
        Starting with a root, pop the root out and
        check whether this is in the path. At root,
        no, so append it. Then, find the neighbours
        of this root, append all of them. Then, check
        whether these are visited. If not, append to path.
        visit the vertex of the vertex, until the end
        of the path. Then, go back toh the visited vertex,
        till the neighbours of the root. Stack, first in,
        first come out. It always find the end of the branch.
        '''
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


    # This one is not used. The path generated always has some problem
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
                path, pathminus = self.dfs_recursive(
                    graph, neighbor, path, pathminus)

        return path, pathminus



    def graphForWS_old(self, subnos, dicttree):
        '''
        represent the watershed using a unreachable graph
        wsGraph = {node: [neighbors]}
        '''
        wsGraph = {}
        for sidx in subnos:
            wsGraph[sidx] = [k for k, v in dicttree.items()
                            if v[1] == sidx]

        return wsGraph
