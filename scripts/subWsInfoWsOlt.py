# -*- coding: utf-8 -*-
import copy


class subWsInfoWsOlt():
    def __init__(self, ascInfoWSOlt, subWsVarJSON):

        ## Json file storing all necessary variables
        # After getting the information for routing, it is time
        # to process the information into the json files.
        self.WsJSON = subWsVarJSON
        self.WsJSON, ascInfoWSOlt.wsSubSolOpsLatLon = self.modifywsJSON(
            self.WsJSON, ascInfoWSOlt)


    def modifywsJSON(self, 
                       json,
                    GetSubInfo):
        wssubsolopslatlong = GetSubInfo.wsSubSolOpsLatLon.copy()

        subPath = []
        subPathSign = []
        for sidx in GetSubInfo.subPurePath[::-1]:
            subPath.append(sidx)
        for sidx2 in GetSubInfo.subRouting[::-1]:
            subPathSign.append(sidx2)

        for subid in range(len(subPath)):
            # Add the subarea to the JSON
            subNo = 0
            subNo = int(subPath[subid])

            #print(subid, subNo)
            wssubsolopslatlong[subid+1] = {}

            wssubsolopslatlong[subid+1]['subNorecal'] = subid + 1

            # Append ws sub no to the dictionary
            wssubsolopslatlong[subid+1]['wsno'] = 1
            wssubsolopslatlong[subid+1]['subno'] = subNo

            
            # Subarea information are stored in lists
            # Update subarea NO: for routing 
            json['tempws']['model_setup'][
                'subid_snum'].append(subid + 1)

            # Update description line:
            json['tempws']['model_setup'][
                'description_title'].append(subNo)

            # Updating Latitude and longitude
            json['tempws']['geographic']['latitude_xct'
                ].append(GetSubInfo.subLatLong[subNo][0])
            json['tempws']['geographic']['longitude_yct'
                ].append(GetSubInfo.subLatLong[subNo][1])
            json['tempws']['geographic']['subarea_elev_sael'
                ].append(GetSubInfo.avgElev[str(subNo)])
            # Append iops no to the dictionary
            wssubsolopslatlong[subid+1]['lat'] = GetSubInfo.subLatLong[subNo][0]
            wssubsolopslatlong[subid+1]['lon'] = GetSubInfo.subLatLong[subNo][1]


            # Updating Average upland slope
            slplen = 0.0
            slplen = GetSubInfo.avgSlope[str(subNo)]

            if (slplen > 50.0):
                json['tempws']['geographic']['avg_upland_slp'
                    ].append(50.0)
            elif( (slplen > 0.0) and (slplen <= 80.0)):
                json['tempws']['geographic']['avg_upland_slp'
                    ].append(slplen)
            else:
                json['tempws']['geographic']['avg_upland_slp'
                    ].append(5.0)

            # Updating Average upland slope length
            json['tempws']['geographic']['avg_upland_slplen_splg'
                ].append(GetSubInfo.avgSlpLen[str(subNo)])            

            # Updating Manning N upland
            # tempCSS: temp list storing the crop soil slope
            # combination [sub, nass lu, soil mukey, slop group]
            tempCSS = []
            tempCSS = GetSubInfo.subCSSMaxDict[subNo]
            json['tempws']['geographic']['uplandmanningn_upn'
                ].append(GetSubInfo.nassLuMgtUpn[tempCSS[1]][12])

            # Updating soil id
            json['tempws']['soil']['soilid'
                ].append(subid+1)

            # Append soil no to the dictionary
            wssubsolopslatlong[subid+1]['mukey'] = tempCSS[2]

            # Update IOPS NO
            json['tempws']['management']['opeartionid_iops'
                ].append(subid+1)
            json['tempws']['management']['OPSName_Reference'
                ].append(GetSubInfo.nassLuMgtUpn[tempCSS[1]][3])


            # Append iops no to the dictionary
            wssubsolopslatlong[subid+1]['iopsno'] = GetSubInfo.nassLuMgtUpn[tempCSS[1]][4]
            wssubsolopslatlong[subid+1]['iopsnm'] = GetSubInfo.nassLuMgtUpn[tempCSS[1]][3]
            # Updating land use no
            # There are other conditions, we will use the first
            # as default. TODO: may need to refine this later.
            json['tempws']['land_use_type']['land_useid_luns'
                ].append(GetSubInfo.nassLuMgtUpn[tempCSS[1]][5])

            # Updating Channel slope:TODO: Calculate the channel and
            # Reach slope later some how
            #print(GetSubInfo.strmAtt[subNo][10])
            json['tempws']['geographic']['channelslope_chs'
                ].append(GetSubInfo.strmAtt[str(subNo)][10])

            # Updating Reach slope: 
            json['tempws']['geographic']['reach_slope_rchs'
                ].append(GetSubInfo.strmAtt[str(subNo)][10])

            # Updating Channel manning n
            json['tempws']['geographic']['channelmanningn_chn'
                ].append(GetSubInfo.channelManN[0][4])


            subarea_area = 0.0
            subarea_area = GetSubInfo.subareaArea[str(subNo)]*GetSubInfo.cellsize*GetSubInfo.cellsize/10000.0
            rchchllen = 0.0
            chllen = 0.0
            rchchllen = GetSubInfo.rchchannenLen[str(subNo)]/1000.0
            chllen = GetSubInfo.channenLen[str(subNo)]/1000.0
            # make sure we have value not 0, had a minimum of 30 m
            if (rchchllen < 0.03):
                rchchllen = 0.03
            if (chllen < 0.03):
                chllen = 0.03 
            if (rchchllen >= chllen):
                chllen = rchchllen + 0.01

            if (subarea_area < 20.0):
                # Updating Channel Length and reach length
                # Reach (stream in TauDEM) length: strmAtt[str(subNo)][6]
                # If it is an extreme watershed, channel length is the max Plen
                if ((GetSubInfo.strmAtt[str(subNo)][2] == '-1')
                    and (GetSubInfo.strmAtt[str(subNo)][3] == '-1')):
                    json['tempws']['geographic']['channellength_chl'
                     ].append(0.5)
                    json['tempws']['geographic']['reach_length_rchl'
                     ].append(0.5)

                # If it is a routing watershed, channel length is the reach len
                # + max channel TODO: will be modified to get the channel length
                # for the watershed outlet
                else:
                    json['tempws']['geographic']['channellength_chl'
                        ].append(0.8)
                    json['tempws']['geographic']['reach_length_rchl'
                        ].append(0.5)

            else:
                # Updating Channel Length and reach length
                # Reach (stream in TauDEM) length: strmAtt[str(subNo)][6]
                # If it is an extreme watershed, channel length is the max Plen
                if ((GetSubInfo.strmAtt[str(subNo)][2] == '-1')
                    and (GetSubInfo.strmAtt[str(subNo)][3] == '-1')):
                    json['tempws']['geographic']['channellength_chl'
                        ].append(rchchllen)
                    json['tempws']['geographic']['reach_length_rchl'
                        ].append(rchchllen)

                # If it is a routing watershed, channel length is the reach len
                # + max channel TODO: will be modified to get the channel length
                # for the watershed outlet
                else:
                    json['tempws']['geographic']['channellength_chl'
                        ].append(chllen)
                    json['tempws']['geographic']['reach_length_rchl'
                        ].append(rchchllen)            

            # Updating Watershed area:
            #print(float(GetSubInfo.subareaArea[str(subNo)])*GetSubInfo.cellsize/10000.0)
            # The area for adding should be minus
            if '-' in subPathSign[subid]:
                json['tempws']['geographic']['wsa_ha'
                    ].append('-%.5f' %(GetSubInfo.subareaArea[str(subNo)]
                         *GetSubInfo.cellsize*GetSubInfo.cellsize/10000.0))
            else:
                json['tempws']['geographic']['wsa_ha'
                ].append('%.5f' %(GetSubInfo.subareaArea[str(subNo)]
                         *GetSubInfo.cellsize*GetSubInfo.cellsize/10000.0))           

            # At this time, tile drainage is sitll unknow, but need to be 
            # initiated.
            json['tempws']['drainage']['drainage_depth_idr'
                ].append('0')
                   
        return json, wssubsolopslatlong






