# -*- coding: utf-8 -*-
from userinputs import userinputs
from .utmconversion import to_latlon, from_latlon, latlon_to_zone_number, latitude_to_zone_letter
from .utmerror import OutOfRangeError

from .globalsetting import globalsetting
from .generalfuncs import generalfuncs
from .gdalfuncs import gdalfuncs
from .solfuncs import solfuncs
from .sqldbfuncs import sqldbfuncs
from .climfuncs import climfuncs


from shutil import copyfile
import numpy as np
import pandas as pd
from osgeo import gdal, ogr
import sys,os
import time
import json
import copy
import glob
import shutil
import subprocess
import copy

globalsetting = globalsetting()
generalfuncs = generalfuncs()
gdalfuncs = gdalfuncs()
solfuncs = solfuncs()
sqldbfuncs = sqldbfuncs()
climfuncs = climfuncs()



class apexfuncs:
    """Various utilities."""
    ##########################################################################
    def updatejson_sit(self, json_sit, infosrc):
        
        json_sit["model_setup"]["siteid"]= "1"
        json_sit["model_setup"]["description_line1"]= "Site1"
        json_sit["model_setup"]["generation_date"]= time.strftime("%d/%m/%Y") 
        json_sit["model_setup"]["nvcn"]= "4"
        json_sit["model_setup"]["outflow_release_method_isao"]= "0"

        json_sit["geographic"]["latitude_ylat"]= infosrc[
                "watershed1"]["geographic"]["latitude_xct"][0]
        json_sit["geographic"]["longitude_xlog"]= infosrc[
                "watershed1"]["geographic"]["longitude_yct"][0]
        json_sit["geographic"]["elevation_elev"]= infosrc[
                "watershed1"]["geographic"]["subarea_elev_sael"][0]

        json_sit["runoff"]["peakrunoffrate_apm"]= "1.00"
        json_sit["co2"]["co2conc_atmos_co2x"]= "330.00"
        json_sit["nitrogen"]["no3n_irrigation_cqnx"]= "0.00"
        json_sit["nitrogen"]["nitrogen_conc_rainfall_rfnx"]= "0.00"
        json_sit["manure"]["manure_p_app_upr"]= "0.00"
        json_sit["manure"]["manure_n_app_unr"]= "0.00"
        json_sit["irrigation"]["auto_irrig_adj_fir0"]= "0.00"
        json_sit["channel"]["basin_channel_length_bchl"] = infosrc[
                "watershed1"]["geographic"]["channellength_chl"][0]
        json_sit["channel"]["basin_chalnel_slp_bchs"]= infosrc[
                "watershed1"]["geographic"]["channelslope_chs"][0]

        return json_sit


    # ##########################################################################
    # def writeSOL(self, jsonsoltemplate, jsonsolscentemp,
    #                  fdApexTio, jsonwssubsollulatlon, fnsolcomfi,
    #                  jsonsolscenrun):
    #     """
    #     This function copy the json template into the 
    #     apex scenario run folder, extract soil property values from the 
    #     database and write them into APEX required sol files.
    #     """
    #     # Copy template sol json to run folder
    #     copyfile(jsonsoltemplate, 
    #             jsonsolscentemp)

    #     # Call soil function to write the SOLCOM file
    #     solfuncs.writeSolCOM(fdApexTio,
    #                 jsonwssubsollulatlon,
    #                 fnsolcomfi)
        
    #     # Create a runsol.json as a template soil json conatining
    #     # template for each soil. The value will be updated in the
    #     # next step.
    #     # Updating nested value in Python is not running correct, I will create
    #     # an empty dictionary, update the value, and then combine them.
    #     # Read in two json files
    #     # Read in the soillu for watershed json
    #     with open(jsonwssubsollulatlon) as json_file:
    #         sollujson = json.loads(json_file.read())
    #     json_file.close()

    #     # Read in the template soil json
    #     with open(jsonsolscentemp) as json_file:
    #         tmpjson = json.loads(json_file.read())
    #     json_file.close()        


    #     sollst = []
    #     for k, v in sollujson.items():
    #         if not v['mukey'] in sollst:
    #             sollst.append(v['mukey'])

    #     # An empty template json to store all updated json
    #     allupdatedsoljson = {}

    #     for solid in sollst:
    #         # Update the variable
    #         temp1sol = None
    #         temp1sol = copy.deepcopy(tmpjson)

    #         temp1sol = solfuncs.update1soljson(sqldbfuncs.sqlconn,
    #                                             "soil1", 
    #                                             solid,
    #                                             temp1sol,
    #                                             sqldbfuncs.dbsoter2apex)
    #         allupdatedsoljson[solid] = temp1sol["soil1"]

    #     with open(jsonsolscenrun, 'w') as outrunsoljson:
    #         json.dump(allupdatedsoljson, outrunsoljson)

    #     # Transfer the runsol json into APEXSOL files
    #     for mkey, solvalue in allupdatedsoljson.items():
    #         solfuncs.writejson2sol(fdApexTio, 
    #                                 solvalue)

    ##########################################################################
    def writeSITCOMandFile(self, jsonSITSce, fnpSitCOM, fnpSit):
        """
        This function write the site list (SITCOM) and individual files.
        """
        # Read in the site file
        with open(jsonSITSce) as json_file:    
            inf_usrjson = json.loads(json_file.read())
        json_file.close()

        fidsitcom = open(fnpSitCOM, "w")
        fidsitcom.writelines("%5i\tSIT%s.SIT\n" %(1,1))
        fidsitcom.close()

        # Write the Site file
        outfid_sit = open(fnpSit, "w")
        # APEXRUN is read with free format in APEX.exe
        # Write line 1:
        outfid_sit.writelines("%s\n".rjust(74, " ") %(fnpSit[:-4]))
        # Write line 2:
        outfid_sit.writelines("%s\n".rjust(70, " ") %(fnpSit))
        # Write line 3:
        outfid_sit.writelines("Outlet 1\n".rjust(74, " "))
        # Write line 4
        outfid_sit.writelines(u"%8.3f%8.3f%8.2f%8s%8s%8s%8s%8s%8s%8s\n" %(\
                            float(inf_usrjson["geographic"]["latitude_ylat"]),\
                            float(inf_usrjson["geographic"]["longitude_xlog"]),\
                            float(inf_usrjson["geographic"]["elevation_elev"]),\
                            inf_usrjson["runoff"]["peakrunoffrate_apm"],\
                            inf_usrjson["co2"]["co2conc_atmos_co2x"],\
                            inf_usrjson["nitrogen"]["no3n_irrigation_cqnx"],\
                            inf_usrjson["nitrogen"]["nitrogen_conc_rainfall_rfnx"],\
                            inf_usrjson["manure"]["manure_p_app_upr"],\
                            inf_usrjson["manure"]["manure_n_app_unr"],\
                            inf_usrjson["irrigation"]["auto_irrig_adj_fir0"]\
                            ))
        # Write Line 5
        outfid_sit.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8.2f%8.2f\n" %(\
                            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,\
                            float(inf_usrjson["channel"]["basin_channel_length_bchl"]),\
                            float(inf_usrjson["channel"]["basin_chalnel_slp_bchs"])\
                            ))
        # Write Line 6
        outfid_sit.writelines("\n")
        # Write Line 7
        outfid_sit.writelines("%8i%8i%8i%8i%8i%8i%8i%8i%8i%8i\n" %(\
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0\
                            ))
        # Write Line 8
        outfid_sit.writelines("%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n" %(\
                            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,0.00, 0.00\
                            ))
        # Write Line 9
        outfid_sit.writelines("\n")     
        # Write Line 10
        outfid_sit.writelines("\n")  
        # Write Line 11
        outfid_sit.writelines("\n")       
         
        outfid_sit.close()


    def copyOPSFiles(self, fdopssrc, fdApexTio):
        """
        This function copy the opsc files to the apexrun folder.
        TODO: This function will be added later when we have 
        an interface to edit the management (OPS) files.
        """
        opsfiles = glob.glob("%s/*" %(fdopssrc))
        for opf in opsfiles:
            opsfilename = os.path.split(opf)[1]
            fnopsdest = os.path.join(fdApexTio,
                                opsfilename)
            # To prevent error, delete file if exist
            if os.path.isfile(fnopsdest):
                os.remove(fnopsdest)
            # Copy
            if not os.path.isfile(opf):
                print("""OPS file {} does not exist. Please check!""".format(
                    opsfilename))
                exit()
            else:
                print(opf)
                shutil.copyfile(opf, fnopsdest)



    def writeSUBCOMandFile(self):
        """
        This function write the Subarea list (SITCOM) and individual files.
        """
        # Read in the site file
        with open(userinputs.jsonrunsubscen) as json_file:    
            subjson = json.loads(json_file.read())
        json_file.close()

        # Write the subacom file
        if os.path.isfile(userinputs.fnsubacom):
            os.remove(userinputs.fnsubacom)
            
        fidsubcom = open(userinputs.fnsubacom, "w")
        for wsid in range(len(subjson.keys())):
            fidsubcom.writelines("%5i\tSUB%s.SUB\n" %(wsid+1,
                                              wsid+1))
        fidsubcom.close()

        # Write the individual subarea files
        for key, value in subjson.items():
            wsid = key[9:]
            self.writefile_sub(wsid, value, userinputs.fdApexTio)


    def writefile_sub(self, wsid, subjson, runfd):
        
        outfn_sub = "SUB%s.SUB" %(wsid)
        # Write the Site file
        if os.path.isfile(outfn_sub):
            os.remove(outfn_sub)
        outfid_sub = open(r"%s/%s" %(runfd, 
                                     outfn_sub), "w")
        # APEXRUN is read with free format in APEX.exe
        # Write line 1:
        # Line 1: format: READ(KR(5),'(I8)')NBSA(ISA)
        totalsubs = len(subjson['model_setup']['subid_snum'])
        for subid in range(totalsubs):
            outfid_sub.writelines("%8s%8s\n" %(
                    subjson['model_setup']['subid_snum'][subid],
                    subjson['model_setup']['description_title'][subid]))
            # Write line 2:
            # Line 2: READ(KR(5),*)INPS,IOPS,IOW,II,IAPL(ISA),I1,NVCN(ISA),IWTH(ISA),&
            # IPTS(ISA),ISAO(ISA),LUNS(ISA),IMW(ISA)
            # 12 variables, free format
            """
            From source code: Nov 20, 2019
            ! SUBAREA DATA
              !  1  INPS = SOIL # FROM TABLE KR(13)
              !  2  IOPS = OP SCHED # FROM TABLE KR(15)
              !  3  IOW  = OWNER ID #
              !  4  II   = 0 FOR NON FEEDING AREAS
              !          = HERD # FOR FEEDING AREAS
              !  5  IAPL = 0 FOR NON MANURE APPL AREAS
              !          = - FEED AREA ID # FOR LIQUID MANURE APPL AREAS
              !          =   FEED AREA ID # FOR SOLID MANURE APPL AREAS
              !  6  NOT USED
              !  7  NVCN = 0 VARIABLE DAILY CN NONLINEAR CN/SW WITH DEPTH SOIL WATER
              !              WEIGHTING
              !          = 1 VARIABLE DAILY CN NONLINEAR CN/SW NO DEPTH WEIGHTING
              !          = 2 VARIABLE DAILY CN LINEAR CN/SW NO DEPTH WEIGHTING
              !          = 3 NON-VARYING CN--CN2 USED FOR ALL STORMS
              !          = 4 VARIABLE DAILY CN SMI(SOIL MOISTURE INDEX)
              !  8  IWTH = INPUT DAILY WEATHER STATION NUMBER
              !  9  IPTS = POINT SOURCE NUMBER
              ! 10  ISAO = 0 FOR NORMAL RES PRINCIPAL SPILLWAY RELEASE
              !          = ID OF SUBAREA RECEIVING OUTFLOW FROM BURRIED PIPE OUTLET
              ! 11  LUNS = LAND USE NUMBER FROM NRCS LAND USE-HYDROLOGIC SOIL GROUP
              !            TABLE.  OVERRIDES LUN IN .OPC FILE.  
              ! 12  IMW  = MIN INTERVAL BETWEEN AUTO MOW
            """
            outfid_sub.writelines(u"%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s\n" %(\
                    str(subjson["soil"]["soilid"][subid]),\
                    str(subjson["management"]["opeartionid_iops"][subid]),\
                    str(subjson["model_setup"]["owner_id"]),\
                    str(subjson["grazing"]["feeding_area_ii"]),\
                    str(subjson["grazing"]["manure_app_area_iapl"]),\
                    '0',\
                    str(subjson["model_setup"]["nvcn"]),\
                    str(subjson["weather"]["daily_wea_stnid_iwth"]),\
                    str(subjson["point_source"]["point_source_ipts"]),\
                    str(subjson["model_setup"]["outflow_release_method_isao"]),\
                    str(subjson["land_use_type"]["land_useid_luns"][subid]),\
                    str(subjson["management"]["min_days_automow_imw"])\
                    ))
            # Write line 3:
            # Line 3: READ(KR(5),*)SNO(ISA),STDO(ISA),YCT(ISA),XCT(ISA),AZM,SAEL,FL,FW,ANGL
            # 9 variables, free format
            """
            From source code: Nov 20, 2019
            ! SUBAREA DATA
            !  1  SNO  = WATER CONTENT OF SNOW COVER(mm)
            !  2  STDO = STANDING DEAD CROP RESIDUE(t/ha)
            !  3  YCT  = LATITUDE OF SUBAREA CENTROID
            !  4  XCT  = LONGITUDE OF SUBAREA CENTROID
            !  5  AZM  = AZIMUTH ORIENTATION OF LAND SLOPE (DEGREES CLOCKWISE FROM NORTH)
            !  6  SAEL = SUBAREA ELEVATION(m)
            !  7  FL   = FIELD LENGTH(km)(0 IF UNKNOWN)
            !  8  FW   = FIELD WIDTH(km)(0 IF UNKNOWN)
            !  9  ANGL = CLOCKWISE ANGLE OF FIELD LENGTH FROM NORTH(deg)(0 IF
            !            UNKNOWN)
            """
            
            outfid_sub.writelines(u"%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(\
                    float(subjson["weather"]["begin_water_in_snow_sno"]),\
                    float(subjson["land_use_type"]["standing_crop_residue_stdo"]),\
                    float(subjson["geographic"]["latitude_xct"][subid]),\
                    float(subjson["geographic"]["longitude_yct"][subid]),\
                    float(subjson["geographic"]["subarea_elev_sael"][subid]),\
                    float(subjson["wind_erosion"]["azimuth_land_slope_azm"]),\
                    float(subjson["wind_erosion"]["field_lenthkm_fl"]),\
                    float(subjson["wind_erosion"]["field_widthkm"]),\
                    float(subjson["wind_erosion"]["angel_of_fieldlength_angl"])\
                    ))
            # Write line 4
            # Line 4: READ(KR(5),*)WSA(ISA),CHL(ISA),CHD,CHS(ISA),CHN(ISA),STP(ISA),&
            # Line 4: SPLG(ISA),UPN,FFPQ(ISA),URBF(ISA)
            """
            ! CATCHMENT CHARACTERISTICS
            !  1  WSA  = DRAINAGE AREA(ha)
            !  2  CHL  = CHANNEL LENGTH(km)(0 IF UNKNOWN)
            !  3  CHD  = CHANNEL DEPTH(m)(0 IF UNKNOWN)
            !  4  CHS  = CHANNEL SLOPE(m/m)(0 IF UNKNOWN)
            !  5  CHN  = MANNINGS N FOR CHANNEL(0 IF UNKNOWN)
            !  6  STP  = AVE UPLAND SLOPE(m/m)
            !  7  SPLG = AVE UPLAND SLOPE LENGTH(m)
            !  8  UPN  = MANNINGS N FOR UPLAND(0 IF UNKNOWN)
            !  9  FFPQ = FRACTION FLOODPLAIN FLOW--PARTITIONS FLOW THRU FILTER STRIPS
            ! 10  URBF = URBAN FRACTION OF SUBAREA
            !     LINE 4
            """
            outfid_sub.writelines(u"%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(\
                    float(subjson["geographic"]["wsa_ha"][subid]),\
                    float(subjson["geographic"]["channellength_chl"][subid]),\
                    float(subjson["geographic"]["channel_depth_chd"]),\
                    float(subjson["geographic"]["channelslope_chs"][subid]),\
                    float(subjson["geographic"]["channelmanningn_chn"][subid]),\
                    float(subjson["geographic"]["avg_upland_slp"][subid]),\
                    float(subjson["geographic"]["avg_upland_slplen_splg"][subid]),\
                    float(subjson["geographic"]["uplandmanningn_upn"][subid]),\
                    float(subjson["flood_plain"]["flood_plain_frac_ffpq"]),\
                    float(subjson["urban"]["urban_frac_urbf"])\
                    ))
            # Write Line 5
            # Line 5: READ(KR(5),*)RCHL(ISA),RCHD(ISA),RCBW(ISA),RCTW(ISA),RCHS(ISA),&
            # Line 5: RCHN(ISA),RCHC(ISA),RCHK(ISA),RFPW(ISA),RFPL(ISA),SAT1,FPS1
            """
            ! CHANNEL GEOMETRY OF ROUTING REACH THRU SUBAREA
            !  1  RCHL = CHANNEL LENGTH OF ROUTING REACH(km)
            !  2  RCHD = CHANNEL DEPTH(m)(0 IF UNKNOWN)
            !  3  RCBW = BOTTOM WIDTH OF CHANNEL(m)(0 IF UNKNOWN)
            !  4  RCTW = TOP WIDTH OF CHANNEL(m)(0 IF UNKNOWN)
            !  5  RCHS = CHANNEL SLOPE(m/m)(0 IF UNKNOWN)
            !  6  RCHN = MANNINGS N VALUE OF CHANNEL(0 IF UNKNOWN)
            !  7  RCHC = USLE C FOR CHANNEL
            !  8  RCHK = USLE K FOR CHANNEL
            !  9  RFPW = FLOODPLAIN WIDTH(m)(0 IF UNKNOWN)
            ! 10  RFPL = FLOODPLAIN LENGTH(km)(0 IF UNKNOWN)
            ! 11  SAT1 = SATURARTED CONDUCTIVITY(GREEN & AMPT) ADJUSTMENT FACTOR(.01_10.)
            ! 12  FPS1 = FLOODPLAIN SATURARTED CONDUCTIVITY ADJUSTMENT FACTOR(.0001_10.)
            """
            outfid_sub.writelines(u"%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(\
                    float(subjson["geographic"]["reach_length_rchl"][subid]),\
                    float(subjson["geographic"]["reach_depth_rchd"]),\
                    float(subjson["geographic"]["reach_bottom_width_rcbw"]),\
                    float(subjson["geographic"]["reach_top_width_rctw"]),\
                    float(subjson["geographic"]["reach_slope_rchs"][subid]),\
                    float(subjson["geographic"]["reach_manningsn_rchn"]),\
                    float(subjson["geographic"]["reach_uslec_rchc"]),\
                    float(subjson["geographic"]["reach_uslek_rchk"]),\
                    float(subjson["geographic"]["reach_floodplain_rfpw"]),\
                    float(subjson["geographic"]["reach_floodplain_length_rfpl"]),\
                    float(subjson["geographic"]["rch_ksat_adj_factor_sat1"]),\
                    float(subjson["flood_plain"]["fp_ksat_adj_factor_fps1"])\
                    ))
            # Write Line 6
            # Line 6 and 7: READ(KR(5),*)RSEE(ISA),RSAE(ISA),RVE0(ISA),RSEP(ISA),&
            # Line 6 and 7:   RSAP(ISA),RVP0(ISA),RSV(ISA),RSRR(ISA),RSYS(ISA),RSYN(ISA),&
            # Line 6 and 7:   RSHC(ISA),RSDP(ISA),RSBD(ISA),PCOF(ISA),BCOF(ISA),&
            # Line 6 and 7:   BFFL(ISA),WTMN(ISA),WTMX(ISA),WTBL(ISA),GWST(ISA),&
            # Line 6 and 7:   GWMX(ISA),RFTT(ISA),RFPK(ISA)
            """
            !  1  RSEE = ELEV AT EMERGENCY SPILLWAY ELEV(m)
            !  2  RSAE = SURFACE AREA AT EMERGENCY SPILLWAY ELEV(ha)
            !  3  RVE0 = VOLUME AT EMERGENCY SPILLWAY ELEV(mm)
            !  4  RSEP = ELEV AT PRINCIPAL SPILLWAY ELEV(m)
            !  5  RSAP = SURFACE AREA AT PRINCIPAL SPILLWAY ELEV(ha)
            !  6  RVP0 = VOLUME AT PRINCIPAL SPILLWAY ELEV(mm)
            !  7  RSV  = INITIAL VOLUME(mm)
            !  8  RSRR = TIME TO RELEASE FLOOD STORAGE(d)
            !  9  RSYS = INITIAL SEDIMENT CONCENTRATION(ppm)
            ! 10  RSYN = NORMAL SEDIMENT CONC(ppm)
            ! 11  RSHC = BOTTOM HYDRAULIC CONDUCTIVITY(mm/h)
            ! 12  RSDP = TIME REQUIRED TO RETURN TO NORMAL SED CONC AFTER RUNOFF
            !            EVENT(d)
            ! 13  RSBD = BULK DENSITY OF SEDIMENT IN RESERVOIR(t/m^3)
            ! 14  PCOF = FRACTION OF SUBAREA CONTROLLED BY PONDS
            ! 15  BCOF = FRACTION OF SUBAREA CONTROLLED BY BUFFERS
            ! 16  BFFL = BUFFER FLOW LENGTH (m)
            ! 17  WTMN = MIN DEPTH TO WATER TABLE(m)(0 IF UNKNOWN)
            ! 18  WTMX = MAX DEPTH TO WATER TABLE(m)(0 IF UNKNOWN)
            ! 19  WTBL = INITIAL WATER TABLE HEIGHT(m)(0 IF UNKNOWN)
            ! 20  GWST = GROUNDWATER STORAGE (mm)
            ! 21  GWMX = MAXIMUM GROUNDWATER STORAGE (mm)
            ! 22  RFTT = GROUNDWATER RESIDENCE TIME(d)(0 IF UNKNOWN)
            ! 23  RFPK = RETURN FLOW / (RETURN FLOW + DEEP PERCOLATION)            """            
            outfid_sub.writelines(u"%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(\
                    float(subjson["reservoir"]["elev_emers_rsee"]),\
                    float(subjson["reservoir"]["res_area_emers_rsae"]),\
                    float(subjson["reservoir"]["runoff_emers_rsve"]),\
                    float(subjson["reservoir"]["elev_prins_rsep"]),\
                    float(subjson["reservoir"]["res_area_prins_rsap"]),\
                    float(subjson["reservoir"]["runoff_prins_rsvp"]),\
                    float(subjson["reservoir"]["ini_res_volume_rsv"]),\
                    float(subjson["reservoir"]["avg_prins_release_rate_rsrr"]),\
                    float(subjson["reservoir"]["ini_sed_res_rsys"]),\
                    float(subjson["reservoir"]["ini_nitro_res_rsyn"])\
                    ))
            # Write Line 7
            outfid_sub.writelines(u"%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(\
                    float(subjson["reservoir"]["hydro_condt_res_bottom_rshc"]),\
                    float(subjson["reservoir"]["time_sedconc_tonormal_rsdp"]),\
                    float(subjson["reservoir"]["bd_sed_res_rsbd"]),\
                    float(subjson["pond"]["frac_pond_pcof"]),\
                    float(subjson["buffer"]["frac_buffer_bcof"]),\
                    float(subjson["buffer"]["buffer_flow_len_bffl"]),\
                    float(subjson["water_table"]["min_watertable_wtmn"]),\
                    float(subjson["water_table"]["max_watertable_wtmx"]),\
                    float(subjson["water_table"]["initial_watertable_wtbl"]),\
                    float(subjson["water_table"]["ground_waterstorage_gwst"]),\
                    float(subjson["water_table"]["maxground_waterstorage_gwmx"]),\
                    float(subjson["water_table"]["groundwater_residencetime_rftt"]),\
                    float(subjson["water_table"]["returnflowfraction_rfpk"])\
                    ))
            # Write Line 8
            # Line 8: READ(KR(5),*)IRR(ISA),IRI(ISA),IFA(ISA),LM(ISA),IFD(ISA),IDR&                                               
            # Line 8: (ISA),(IDF0(I,ISA),I=1,6),IRRS(ISA),IRRW(ISA)
            """
            !     READ MANAGEMENT INFORMATION                                                                           
            !  1  IRR  = N0 FOR DRYLAND AREAS          | N = 0 APPLIES MINIMUM OF                                       
            !          = N1 FROM SPRINKLER IRRIGATION  | VOLUME INPUT, ARMX, & FC-SW                                    
            !          = N2 FOR FURROW IRRIGATION      | N = 1 APPLIES INPUT VOLUME                                     
            !          = N3 FOR IRR WITH FERT ADDED    | OR ARMX                                                        
            !          = N4 FOR IRRIGATION FROM LAGOON |                                                                
            !          = N5 FOR DRIP IRR               |                                                                
            !  2  IRI  = N DAY APPLICATION INTERVAL FOR AUTOMATIC IRRIGATION                                            
            !  3  IFA  = MIN FERT APPL INTERVAL(0 FOR USER SPECIFIED)                                               
            !  4  LM   = 0 APPLIES LIME                                                                                 
            !          = 1 DOES NOT APPLY LIME                                                                          
            !  5  IFD  = 0 WITHOUT FURROW DIKES                                                                         
            !            1 WITH FURROW DIKES                                                                            
            !  6  IDR  = 0 NO DRAINAGE                                                                                  
            !          = DEPTH OF DRAINAGE SYSTEM(mm)                                                                   
            !     IDF0 = FERT #                                                                                         
            !  7         1 FOR FERTIGATION FROM LAGOON                                                                  
            !  8         2 FOR AUTOMATIC SOLID MANURE APPL FROM FEEDING AREA STOCK                                      
            !              PILE.                                                                                        
            !  9         3 AUTO COMERCIAL P FERT APPL (DEFAULTS TO ELEM P)                                              
            !  10        4 FOR AUTOMATIC COMERCIAL FERT APPL(DEFALTS TO ELEM N)                                         
            !  11        5 FOR AUTOMATIC SOLID MANURE APPLICATION.                                                      
            !  12        6 AUTO COMERCIAL K FERT APPL (DEFAULTS TO ELEM K)                                              
            !  13 IRRS = ID OF SA SUPPLYING IRRIGATION WATER FROM A RESERVOIR                                           
            !            0 NO RESERVOIR SUPPLY OR NO IRRIGATION
            !  14 IRRW = ID OF SA SUPPLYING IRRIGATION WATER FROM A WELL
            !            0 NO WELL SUPPLY
            !     LINE 8 
            """
            outfid_sub.writelines(u"%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s\n" %(\
                    str(subjson["irrigation"]["irrigation_irr"]),\
                    str(subjson["irrigation"]["min_days_btw_autoirr_iri"]),\
                    str(subjson["management"]["min_days_autonitro_ifa"]),\
                    str(subjson["management"]["liming_code_lm"]),\
                    str(subjson["management"]["furrow_dike_code_ifd"]),\
                    str(subjson["drainage"]["drainage_depth_idr"][subid]),\
                    str(subjson["management"]["autofert_lagoon_idf1"]),\
                    str(subjson["management"]["auto_manure_feedarea_idf2"]),\
                    str(subjson["management"]["auto_commercial_p_idf3"]),\
                    str(subjson["management"]["auto_commercial_n_idf4"]),\
                    str(subjson["management"]["auto_solid_manure_idf5"]),\
                    str(subjson["management"]["auto_commercial_k_idf6"]),\
                    str(subjson["irrigation"]["subareaid_irrreservior_irrs"]),\
                    str(subjson["irrigation"]["subareaid_irrwell_irrw"])\
                    ))
            # Write Line 9
            # Read Line 9: READ(KR(5),*)BIR(ISA),EFI(ISA),VIMX(ISA),ARMN(ISA),ARMX(ISA),&                                              
            # Read Line 9: BFT(ISA),FNP(4,ISA),FMX,DRT(ISA),FDSF(ISA),PEC(ISA),DALG(ISA),VLGN&                                         
            # Read Line 9: (ISA),COWW(ISA),DDLG(ISA),SOLQ(ISA),SFLG,FNP(2,ISA),FNP(5,ISA),&                                            
            # Read Line 9: FIRG(ISA)  
            """
            !  1  BIR  = IRRIGATION TRIGGER--3 OPTIONS                                                                  
            !            1. PLANT WATER STRESS FACTOR (0-1)                                                             
            !            2. SOIL WATER TENSION IN TOP 200 MM(> 1 KPA)                                                   
            !            3. PLANT AVAILABLE WATER DEFICIT IN ROOT ZONE (-mm)                                            
            !  2  EFI  = RUNOFF VOL / VOL IRR WATER APPLIED(0 IF IRR=0)                                             
            !  3  VIMX = MAXIMUM ANNUAL IRRIGATION VOLUME ALLOWED FOR EACH CROP (mm)                                    
            !  4  ARMN = MINIMUM SINGLE APPLICATION VOLUME ALLOWED (mm)                                                 
            !  5  ARMX = MAXIMUM SINGLE APPLICATION VOLUME ALLOWED (mm)                                                 
            !  6  BFT  = AUTO FERTILIZER TRIGGER--2 OPTIONS                                                             
            !            1. PLANT N STRESS FACTOR (0-1)                                                                 
            !            2. SOIL N CONC IN ROOT ZONE (g/t)                                                              
            !  7  FNP4 = AUTO FERT FIXED APPLICATION RATE (kg/ha)                                                       
            !  8  FMX  = MAXIMUM ANNUAL N FERTILIZER APPLICATION FOR A CROP (kg/ha)                                     
            !  9  DRT  = TIME REQUIRED FOR DRAINAGE SYSTEM TO REDUCE PLANT STRESS(d)                                    
            !            (0 IF DRAINAGE NOT USED)                                                                   
            ! 10  FDSF = FURROW DIKE SAFETY FACTOR(0-1.)                                                                
            ! 11  PEC  = CONSERVATION PRACTICE FACTOR(=0.0 ELIMINATES WATER EROSION)                                    
            ! 12  DALG = FRACTION OF SUBAREA CONTROLLED BY LAGOON.                                                      
            ! 13  VLGN = LAGOON VOLUME RATIO--NORMAL / MAXIMUM                                                          
            ! 14  COWW = LAGOON INPUT FROM WASH WATER (m3/hd/d)                                                         
            ! 15  DDLG = TIME TO REDUCE LAGOON STORAGE FROM MAX TO NORM (d)                                             
            ! 16  SOLQ = RATIO LIQUID/TOTAL MANURE PRODUCED.                                                            
            ! 17  SFLG = SAFETY FACTOR FOR LAGOON DESIGN (VLG=VLG0/(1.-SFLG)                                            
            ! 18  FNP2 = FEEDING AREA STOCK PILE AUTO SOLID MANURE APPL RATE (kg/ha)                                    
            ! 19  FNP5 = AUTOMATIC MANURE APPLICATION RATE (kg/ha)                                                      
            ! 20  FIRG = FACTOR TO ADJUST AUTO IRRIGATION VOLUME (FIRG*FC)                                              
            !     LINE 9/10   
            """
            outfid_sub.writelines(u"%10s%10s%10s%10s%10s%10s%10s%10s%10s%10s\n" %(\
                    str(subjson["irrigation"]["waterstress_triger_irr_bir"]),\
                    str(subjson["irrigation"]["irr_lost_runoff_efi"]),\
                    str(subjson["irrigation"]["max_annual_irri_vol_vimx"]),\
                    str(subjson["irrigation"]["min_single_irrvol_armn"]),\
                    str(subjson["irrigation"]["max_single_irrvol_armx"]),\
                    str(subjson["management"]["nstress_trigger_auton_bft"]),\
                    str(subjson["management"]["auton_rate_fnp4"]),\
                    str(subjson["management"]["max_annual_auton_fmx"]),\
                    str(subjson["drainage"]["drain_days_end_w_stress_drt"]),\
                    str(subjson["management"]["fd_water_store_fdsf"])\
                    )) 
            # Write Line 10

            outfid_sub.writelines(u"%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(\
                    float(subjson["water_erosion"]["usle_p_pec"]),\
                    float(subjson["pond"]["frac_lagoon_dalg"]),\
                    float(subjson["pond"]["lagoon_vol_ratio_vlgn"]),\
                    float(subjson["pond"]["wash_water_to_lagoon_coww"]),\
                    float(subjson["pond"]["time_reduce_lgstorage_nom_ddlg"]),\
                    float(subjson["pond"]["ratio_liquid_manure_to_lg_solq"]),\
                    float(subjson["pond"]["frac_safety_lg_design_sflg"]),\
                    float(subjson["grazing"]["feedarea_pile_autosolidmanure_rate_fnp2"]),\
                    float(subjson["management"]["auton_manure_fnp5"]),\
                    float(subjson["irrigation"]["factor_adj_autoirr_firg"])\
                    ))                        
            # Write Line 11
            # Read line 11:READ(KR(5),*)(NY(J),J=1,NZ)  
            """
            !     NY   = 0 FOR NON GRAZING AREA                                                                         
            !          = HERD NUMBERS FOR GRAZING AREA                                                                  
            !     LINE 11  
            """
            outfid_sub.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
                    str(subjson["grazing"]["herds_eligible_forgrazing_ny1"]),\
                    str(subjson["grazing"]["herds_eligible_forgrazing_ny2"]),\
                    str(subjson["grazing"]["herds_eligible_forgrazing_ny3"]),\
                    str(subjson["grazing"]["herds_eligible_forgrazing_ny4"]),\
                    str(subjson["grazing"]["herds_eligible_forgrazing_ny5"]),\
                    str(subjson["grazing"]["herds_eligible_forgrazing_ny6"]),\
                    str(subjson["grazing"]["herds_eligible_forgrazing_ny7"]),\
                    str(subjson["grazing"]["herds_eligible_forgrazing_ny8"]),\
                    str(subjson["grazing"]["herds_eligible_forgrazing_ny9"]),\
                    str(subjson["grazing"]["herds_eligible_forgrazing_ny10"])\
                    ))                          
            # Write Line 12
            # Read line 12:READ(KR(5),*)(NY(J),J=1,NZ)  
            """
            ! XTP  = GRAZING LIMIT FOR EACH HERD--MINIMUM PLANT MATERIAL(t/ha)                                      
            ! LINE 12  
            """
            outfid_sub.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
                    str(subjson["grazing"]["grazing_limit_herd_xtp1"]),\
                    str(subjson["grazing"]["grazing_limit_herd_xtp2"]),\
                    str(subjson["grazing"]["grazing_limit_herd_xtp3"]),\
                    str(subjson["grazing"]["grazing_limit_herd_xtp4"]),\
                    str(subjson["grazing"]["grazing_limit_herd_xtp5"]),\
                    str(subjson["grazing"]["grazing_limit_herd_xtp6"]),\
                    str(subjson["grazing"]["grazing_limit_herd_xtp7"]),\
                    str(subjson["grazing"]["grazing_limit_herd_xtp8"]),\
                    str(subjson["grazing"]["grazing_limit_herd_xtp9"]),\
                    str(subjson["grazing"]["grazing_limit_herd_xtp10"])\
                    ))                         
                
        outfid_sub.close()


    def copyCONTjson2fdrun(self):
        """
        This function copy the CONT json from data to run folder.
        """
        # To prevent error, delete file if exist
        if os.path.isfile(userinputs.jsonapexcontrun):
            os.remove(userinputs.jsonapexcontrun)
        # Copy
        shutil.copyfile(userinputs.jsonapexconttemp, 
                        userinputs.jsonapexcontrun)



    def writeAPEXCONT(self, JScontRun, fnapexcont, dailyWeaVar, useDlyWea):
        """
        This function write APEXCONT files.
        """
        with open(JScontRun) as json_file:    
            contjs = json.loads(json_file.read())
        json_file.close()

        # Write the APEXCONT file
        if os.path.isfile(fnapexcont):
            os.remove(fnapexcont)
            
        outfid_cont = open(fnapexcont, "w")
		# APEXCONT is read with free format in APEX.exe
		# Line 1 and 2
        # READ(KR(20),*)NBY0,IYR0,IMO,IDA0,IPD,NGN0,IGN,IGSD,LPYR,IET,&
        # ISCN,ITYP,ISTA,IHUS,NVCN0,INFL,MASP,IERT,LBP,NUPC,MNUL,LPD,MSCP,&
        # ISLF,NAQ,IHY,ICO2,ISW,IGMX,IDIR,IMW0,IOX,IDNT,IAZM,IPAT,IHRD,IWTB,&
        # IKAT,NSTP,IPRK,ICP,NTV,IREM,IHAY,ISAP
        """
        !  1  NBY0 = NUMBER OF YEARS OF SIMULATION
        !  2  IYR0 = BEGINNING YEAR OF SIMULATION
        !  3  IMO  = MONTH SIMULATION BEGINS
        !  4  IDA  = DAY OF MONTH SIMULATION BEGINS
        !  5  IPD  = N0 FOR ANNUAL WATERSHED OUTPUT
        !          = N1 FOR ANNUAL OUTPUT                       | N YEAR INTERVAL
        !          = N2 FOR ANNUAL WITH SOIL TABLE              | N=0 SAME AS
        !          = N3 FOR MONTHLY                             | N=1 EXCEPT
        !          = N4 FOR MONTHLY WITH SOIL TABLE             | N=0 PRINTS
        !          = N5 FOR MONTHLY WITH SOIL TABLE AT HARVEST  | OPERATIONS
        !          = N6 FOR N DAY INTERVAL
        !          = N7 FOR SOIL TABLE ONLY N DAY INTERVAL
        !          = N8 FOR SOIL TABLE ONLY DURING GROWING SEASON N DAY INTERVAL
        !          = N9 FOR N DAY INTERVAL DURING GROWING SEASON
        !  6  NGN0 = ID NUMBER OF WEATHER VARIABLES INPUT.  RAIN=1,  TEMP=2,
        !            RAD=3,  WIND SPEED=4,  REL HUM=5.  IF ANY VARIABLES ARE INP
        !            RAIN MUST BE INCLUDED.  THUS, IT IS NOT NECESSARY TO SPECIF
        !            ID=1 UNLESS RAIN IS THE ONLY INPUT VARIABLE.
        !            NGN=-1 ALL VARIABLES GENERATED(SAME VALUES ALL SUBAREAS).
        !            NGN=0  ALL VARIABLES GENERATED(SPATIALLY DISTRIBUTED).  
        !            EXAMPLES
        !            NGN=1 INPUTS RAIN.
        !            NGN=23 INPUTS RAIN, TEMP, AND RAD.
        !            NGN=2345 INPUTS ALL 5 VARIABLES.
        !  7  IGN  = NUMBER TIMES RANDOM NUMBER GEN CYCLES BEFORE
        !            SIMULATION STARTS
        !  8  IGS0 = 0 FOR NORMAL OPERATION OF WEATHER MODEL.
        !          = N NO YRS INPUT WEATHER BEFORE REWINDING (USED FOR REAL TIME
        !            SIMULATION).
        !  9  LPYR = 0 IF LEAP YEAR IS CONSIDERED
        !          = 1 IF LEAP YEAR IS IGNORED
        ! 10  IET  = PET METHOD CODE
        !          = 1 FOR PENMAN-MONTEITH
        !          = 2 FOR PENMAN
        !          = 3 FOR PRIESTLEY-TAYLOR
        !          = 4 FOR HARGREAVES
        !          = 5 FOR BAIER-ROBERTSON
        ! 11  ISCN = 0 FOR STOCHASTIC CURVE NUMBER ESTIMATOR.
        !          > 0 FOR RIGID CURVE NUMBER ESTIMATOR.
        ! 12  ITYP = 0 FOR MODIFIED RATIONAL EQ STOCHASTIC PEAK RATE ESTIMATE.
        !          < 0 FOR MODIFIED RATIONAL EQ RIGID PEAK RATE ESTIMATE.
        !          > 0 FOR SCS TR55 PEAK RATE ESTIMATE.
        !          = 1 FOR TYPE 1 RAINFALL PATTERN
        !          = 2     TYPE 1A
        !          = 3     TYPE 2
        !          = 4     TYPE 3
        !          = 5 FOR SCS UNIT HYD PEAK RATE ESTIMATE
        ! 13  ISTA = 0 FOR NORMAL EROSION OF SOIL PROFILE
        !          = 1 FOR STATIC SOIL PROFILE
        ! 14  IHUS = 0 FOR NORMAL OPERATION
        !          = 1 FOR AUTOMATIC HEAT UNIT SCHEDULE(PHU MUST BE INPUT AT
        !              PLANTING)
        ! 15  NVCN0= 0 VARIABLE DAILY CN NONLINEAR CN/SW WITH DEPTH SOIL WATER
        !              WEIGHTING
        !          = 1 VARIABLE DAILY CN NONLINEAR CN/SW NO DEPTH WEIGHTING
        !          = 2 VARIABLE DAILY CN LINEAR CN/SW NO DEPTH WEIGHTING
        !          = 3 NON-VARYING CN--CN2 USED FOR ALL STORMS
        !          = 4 VARIABLE DAILY CN SMI(SOIL MOISTURE INDEX)
        ! 16  INFL = 0 FOR CN ESTIMATE OF Q
        !          = 1 FOR GREEN & AMPT ESTIMATE OF Q, RF EXP DST, PEAK RF RATE
        !              SIMULATED.
        !          = 2 FOR G&A Q, RF EXP DST, PEAK RF INPUT
        !          = 3 FOR G&A Q, RF UNIFORMLY DST, PEAK RF INPUT
        !          = 4 FOR G&A Q, RF INPUT AT TIME INTERVAL DTHY
        ! 17  MASP = 1 FOR PESTICIDE APPLIED IN g/ha
        !          = 1000 FOR PESTICIDE APPLIED IN kg/ha
        ! 18  IERT = 0 FOR EPIC ENRICHMENT RATIO METHOD
        !          = 1 FOR GLEAMS ENRICHMENT RATIO METHOD
        ! 19  LBP  = 0 FOR SOL P RUNOFF ESTIMATE USING GLEAMS PESTICIDE EQ
        !          = 1 FOR LANGMUIR EQ
        ! 20  NUPC = N AND P PLANT UPTAKE CONCENTRATION CODE
        !          = 0 FOR SMITH CURVE
        !          > 0 FOR S CURVE
        ! 21  MNUL = MANURE APPLICATION CODE
        !          = 0 FOR AUTO APPLICATION TO SUBAREA WITH MINIMUM LAB P CONC
        !          = 1 FOR VARIABLE P RATE LIMITS ON ANNUAL APPLICATION BASED ON
        !            JAN 1 LAB P CONC.
        !          = 2 FOR VARIABLE N RATE LIMITS ON ANNUAL APPLICATION BASED ON
        !            JAN 1 LAB P CONC.
        !          = 3 SAME AS 1 EXCEPT APPLICATIONS OCCUR ON ONE SUBAREA AT A 
        !            TIME UNTIL LAB P CONC REACHES 200 ppm. THEN ANOTHER SUBAREA
        !            IS USED, ETC.
        ! 22  LPD  = DAY OF YEAR TO TRIGGER LAGOON PUMPING DISREGARDING NORMAL
        !            PUMPING TRIGGER--USUALLY BEFORE WINTER OR HIGH RAINFALL 
        !            SEASON.
        !          = 0 DOES NOT TRIGGER EXTRA PUMPING
        ! 23  MSCP = INTERVAL FOR SCRAPING SOLID MANURE FROM FEEDING AREA (d)
        ! 24  ISLF = 0 FOR RUSLE SLOPE LENGTH/STEEPNESS FACTOR
        !          > 0 FOR MUSLE SLOPE LENGTH/STEEPNESS FACTOR
        ! 25  NAQ  > 0 FOR AIR QUALITY ANALYSIS
        !          = 0 NO AIR QUALITY ANALYSIS
        ! 26  IHY  = 0 NO FLOOD ROUTING
        !          = 1 VSC FLOOD ROUTING
        !          = 2 SVS FLOOD ROUTING
        !          = 3 MUSKINGUM-CUNGE VC
        !          = 4 MUSKINGUM-CUNGE M_CVC4 
        ! 27  ICO2 = 0 FOR CONSTANT ATMOSPHERIC CO2
        !          = 1 FOR DYNAMIC ATMOSPHERIC CO2
        !          = 2 FOR INPUTTING CO2
        ! 28  ISW  = 0 FIELD CAP/WILTING PT EST RAWLS METHOD DYNAMIC.
        !          = 1 FIELD CAP/WILTING PT INP RAWLS METHOD DYNAMIC.
        !          = 2 FIELD CAP/WILTING PT EST RAWLS METHOD STATIC.
        !          = 3 FIELD CAP/WILTING PT INP STATIC.
        !          = 4 FIELD CAP/WILTING PT NEAREST NEIGHBOR DYNAMIC
        !          = 5 FIELD CAP/WILTING PT NEAREST NEIGHBOR STATIC
        !          = 6 FIELD CAP/WILTING PT BEHRMAN-NORFLEET-WILLIAMS (BNW) DYNAMIC                         
        !          = 7 FIELD CAP/WILTING PT BEHRMAN-NORFLEET-WILLIAMS (BNW) STATIC
        ! 29  IGMX = # TIMES GENERATOR SEEDS ARE INITIALIZED FOR A SITE.
        ! 30  IDIR = 0 FOR READING DATA FROM WORKING DIRECTORY
        !          > 0 FOR READING FROM WEATDATA DIRECTORY
        ! 31  IMW0 = MIN INTERVAL BETWEEN AUTO MOW 
        ! 32  IOX  = 0 FOR ORIGINAL EPIC OXYGEN/DEPTH FUNCTION
        !          > 0 FOR ARMEN KEMANIAN CARBON/CLAY FUNCTION
        ! 33  IDNT = 1 FOR ORIGINAL EPIC DENITRIFICATION SUBPROGRAM
        !          = 2 FOR ARMEN KEMANIAN DENITRIFICATION SUBPROGRAM
        !          = 3 FOR CESAR IZAURRALDE DENITRIFICATION SUBPROGRAM (ORIGINAL DW)
        !          = 4 FOR CESAR IZAURRALDE DENITRIFICATION SUBPROGRAM (NEW DW)     
        ! 34  IAZM = 0 FOR USING INPUT LATITUDES FOR SUBAREAS
        !          > 0 FOR COMPUTING EQUIVALENT LATITUDE BASED ON AZIMUTH 
        !            ORIENTATION OF LAND SLOPE.
        ! 35  IPAT = 0 TURNS OFF AUTO P APPLICATION
        !          > 0 FOR AUTO P APPLICATION
        ! 36  IHRD = 0 FOR LEVEL 0(MANUAL) GRAZING MODE(NO HERD FILE REQUIRED)
        !          = 1 FOR LEVEL 1(HYBRID) GRAZING MODE(HERD FILE REQUIRED) 
        !          = 2 FOR LEVEL 2(AUTOMATIC) GRAZING MODE(HERD FILE REQUIRED)  
        ! 37  IWTB = DURATION OF ANTEDEDENT PERIOD FOR RAINFALL AND PET 
        !            ACCUMULATION TO DRIVE WATER TABLE.
        ! 38  IKAT = 0 TURNS OFF AUTO K APPLICATION
        !          > 0 FOR AUTO K APPLICATION
        ! 39  NSTP = REAL TIME DAY OF YEAR
        ! 40  IPRK = 0 FOR HPERC 
        !          > 0 FOR HPERC1 (4MM SLUG FLOW)
        ! 41  ICP  = 0 FOR NCNMI_PHOENIX
        !          > 0 FOR NCNMI_CENTURY
        ! 42  NTV  = 0 FOR ORIGINAL APEX NITVOL EQS
        !          > 0 FOR IZAURRALDE REVISED NITVOL EQS
        ! 43  IREM = 0 SSK FROM REMX
        !          > 0 SSK FROM USLE
        ! 44  IHAY = 0 FOR NO HAY FEEDING
        !          > 0 FOR HAY FEEDING WHEN FORAGE IS < GZLM
        ! 45  ISAP = DOUBLE VARIABLE (ISA/IPCD) TO PRINT DAILY BALANCES USING SR NCONT
        !            IPCD=1 FOR C
        !                =2 FOR H2O
        !                =3 FOR P
        !                =4 FOR N
        !            NBSA=SELECTED SA ID #   
        !     LINE 1/2
        """
        # modify the weather input code if user would like to use their own observed data
        if useDlyWea:
            if dailyWeaVar == ["prcp"]:
                contjs["weather"]["weather_in_var_ngn"] = "1"
            elif dailyWeaVar == ["prcp", "tmax", "tmin"]:
                contjs["weather"]["weather_in_var_ngn"] = "2"
            elif dailyWeaVar == ["prcp", "solar"]:
                contjs["weather"]["weather_in_var_ngn"] = "3"
            elif dailyWeaVar == ["prcp", "wind"]:
                contjs["weather"]["weather_in_var_ngn"] = "4"
            elif dailyWeaVar == ["prcp", "rh"]:
                contjs["weather"]["weather_in_var_ngn"] = "5"
            elif dailyWeaVar == ["prcp", "tmax", "tmin", "solar"]:
                contjs["weather"]["weather_in_var_ngn"] = "5"
            elif dailyWeaVar == ["prcp", "tmax", "tmin", "solar", "rh", "wind"]:
                contjs["weather"]["weather_in_var_ngn"] = "2345"
        else:
            contjs["weather"]["weather_in_var_ngn"] = "0"
        
        outfid_cont.writelines(u"%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s\n" %(\
			contjs["model_setup"]["yearstorun_nbyr"],\
			contjs["model_setup"]["begin_year_iyr"],\
			contjs["model_setup"]["begin_month_imo"],\
			contjs["model_setup"]["begin_day_ida"],\
			contjs["model_setup"]["output_freq_ipd"],\
			contjs["weather"]["weather_in_var_ngn"],\
			contjs["weather"]["random_seeds_ign"],\
			contjs["weather"]["date_weather_duplicate_igsd"],\
			contjs["model_setup"]["leap_year_lpyr"],\
			contjs["weather"]["pet_method_iet"],\
			contjs["runoff_sim"]["stochastic_cn_code_iscn"],\
			contjs["runoff_sim"]["peak_rate_method_ityp"],\
			contjs["water_erosion"]["static_soil_code_ista"],\
			contjs["management"]["automatic_hu_schedule_ihus"],\
			contjs["runoff_sim"]["non_varying_cn_nvcn"],\
			contjs["runoff_sim"]["runoff_method_infl"],\
			contjs["nutrient_loss"]["pesticide_mass_conc_masp"],\
			contjs["nutrient_loss"]["enrichment_ratio_iert"],\
			contjs["nutrient_loss"]["soluble_p_estimate_lbp"],\
			contjs["nutrient_loss"]["n_p_uptake_curve_nupc"]\
				))
		# Line 2
        outfid_cont.writelines(u"%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s%5s\n" %(
            contjs["management"]["manure_application_mnul"],\
			contjs["management"]["lagoon_pumping_lpd"],\
			contjs["management"]["solid_manure_mscp"],\
			contjs["water_erosion"]["slope_length_steep_islf"],\
			contjs["air_quality"]["air_quality_code_naq"],\
			contjs["flood_routing"]["flood_routing_ihy"],\
			contjs["air_quality"]["co2_ico2"],\
			contjs["runoff_sim"]["field_capacity_wilting_isw"],\
			contjs["weather"]["number_generator_seeds_igmx"],\
			contjs["model_setup"]["data_dir_idir"],\
			contjs["management"]["minimum_interval_automow_imw"],\
			contjs["air_quality"]["o2_function_iox"],\
			contjs["nutrient_loss"]["denitrification_idnt"],\
			contjs["geography"]["latitude_source_iazm"],\
			contjs["management"]["auto_p_ipat"],\
			contjs["management"]["grazing_mode_ihrd"],\
			contjs["runoff_sim"]["atecedent_period_iwtb"],\
            contjs["newpar201911"]["auto_k_applic_ikat"],\
			contjs["model_setup"]["real_time_nstp"],\
            contjs["newpar201911"]["forhperc_iprk"],\
			contjs["newpar201911"]["ncnmimethod_icp"],\
			contjs["newpar201911"]["nitvolequa_ntv"],\
			contjs["newpar201911"]["sskfromremxorusle_irem"],\
			contjs["newpar201911"]["hayfeeding_ihay"],\
            contjs["model_setup"]["output_subareanum_isap"]\
			))                      
		# Line 3 to 6
        """
        !  1  RFN0 = AVE CONC OF N IN RAINFALL(ppm)
        !  2  CO20 = CO2 CONCENTRATION IN ATMOSPHERE(ppm)
        !  3  CQN0 = CONC OF N IN IRRIGATION WATER(ppm)
        !  4  PSTX = PEST DAMAGE SCALING FACTOR (0.-10.)--0. SHUTS OFF PEST
        !            DAMAGE FUNCTION. PEST DAMAGE FUNCTION CAN BE REGULATED FROM
        !            VERY MILD(0.05-0.1) TO VERY SEVERE(1.-10.)
        !  5  YWI  = NO Y RECORD MAX .5H RAIN(0 IF WI IS NOT
        !            INPUT)
        !  6  BTA  = COEF(0-1)GOVERNING WET-DRY PROBABILITIES GIVEN DAYS
        !            OF RAIN(0 IF UNKNOWN OR IF W|D PROBS ARE
        !            INPUT)
        !  7  EXPK = PARAMETER USED TO MODIFY EXPONENTIAL RAINFALL AMOUNT
        !            DISTRIBUTION(0 IF UNKNOWN OR IF ST DEV & SK CF ARE
        !            INPUT)
        !  8  QG   = 2 YEAR FREQ 24-H RAINFALL (mm)--ESTIMATES REACH CH GEOMETRY
        !            IF UNKNOWN(0 IF CH GEO IS INPUT)
        !  9  QCF  = EXPONENT IN WATERSHED AREA FLOW RATE EQ
        ! 10  CHS0 = AVE UPLAND SLOPE (m/m) IN WATERSHED
        ! 11  BWD  = CHANNEL BOTTOM WIDTH/DEPTH(QG>0)
        ! 12  FCW  = FLOODPLAIN WIDTH/CHANNEL WIDTH
        ! 13  FPS0 = FLOODPLAIN SAT COND ADJUSTMENT FACTOR(.0001_10.)
        ! 14  GWS0 = MAXIMUM GROUNDWATER STORAGE(mm)
        ! 15  RFT0 = GROUNDWATER RESIDENCE TIME(d)
        ! 16  RFP0 = RETURN FLOW / (RETURN FLOW + DEEP PERCOLATION)
        ! 17  SAT0 = SATURARTED CONDUCTIVITY ADJUSTMENT FACTOR(.1_10.)
        ! 18  FL0  = FIELD LENGTH(km)(0 IF UNKNOWN)
        ! 19  FW0  = FIELD WIDTH(km)(0 IF UNKNOWN)
        ! 20  ANG0 = CLOCKWISE ANGLE OF FIELD LENGTH FROM NORTH(deg)(0 IF
        !            UNKNOWN)
        ! 21  UXP  = POWER PARAMETER OF MODIFIED EXP DIST OF WIND SPEED(0
        !            IF UNKNOWN)
        ! 22  DIAM = SOIL PARTICLE DIAMETER(UM)(0 IF UNKNOWN)
        ! 23  ACW  = WIND EROSION CONTROL FACTOR
        !            = 0.0 NO WIND EROSION
        !            = 1.0 FOR NORMAL SIMULATION
        !            > 1.0 ACCELERATES WIND EROSION(CONDENSES TIME)
        ! 24  GZL0 = GRAZING LIMIT--MINIMUM PLANT MATERIAL(t/ha)
        ! 25  RTN0 = NUMBER YEARS OF CULTIVATION AT START OF SIMULATION
        ! 26  BXCT = LINEAR COEF OF CHANGE IN RAINFALL FROM E TO W(PI/P0/KM)
        ! 27  BYCT = LINEAR COEF OF CHANGE IN RAINFALL FROM S TO N(PI/P0/KM)
        ! 28  DTHY = TIME INTERVAL FOR FLOOD ROUTING(h)
        ! 29  QTH  = ROUTING THRESHOLD(mm)--VSC ROUTING USED ON QVOL>QTH
        ! 30  STND = VSC ROUTING USED WHEN REACH STORAGE >STND
        ! 31  DRV  = SPECIFIES WATER EROSION DRIVING EQ.
        !            (1=RUSL2;  2=USLE;  3=MUSS;  4=MUSL;   5=MUST;  6=REMX)
        ! 32  PCO0 = FRACTION OF SUBAREAS CONTROLLED BY PONDS.
        ! 33  RCC0 = REACH CHANNEL USLE C FACTOR
        ! 34  CSLT = SALT CONC IN IRRIGATION WATER (ppm)
        ! 35  CPV0 = FRACTION INFLOW PARTITIONED TO VERTICLE CRACK OR PIPE FLOW
        ! 36  CPH0 = FRACTION INFLOW PARTITIONED TO HORIZONTAL CRACK OR PIPE FLOW 
        ! 37  DZDN = LAYER THICKNESS FOR DIFFERENTIAL EQ SOLN TO GAS DIFF EQS(m)
        ! 38  DTG  = TIME INTERVAL FOR GAS DIFF EQS (h)
        ! 39  QPQ  = RATIO VOLUME BEFORE TP TO TOTAL VOLUME OF UNIT HYD
        """
        outfid_cont.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
			contjs["nutrient_loss"]["avg_conc_n_rainfall_rfn"],\
			contjs["air_quality"]["co2_conc_atom_co2"],\
			contjs["nutrient_loss"]["no3n_conc_irrig_cqn"],\
			contjs["management"]["pest_damage_scaling_pstx"],\
			contjs["weather"]["yrs_max_mon_rainfall_ywi"],\
			contjs["weather"]["wetdry_prob_bta"],\
			contjs["weather"]["param_exp_rainfall_dist_expk"],\
			contjs["runoff_sim"]["channel_capacity_flow_qg"],\
			contjs["runoff_sim"]["exp_watershed_area_flowrate_qcf"],\
			contjs["geography"]["average_upland_slope_chso"]\
			))                                    
		# Line 4
        outfid_cont.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
			contjs["geography"]["channel_bottom_woverd_bwd"],\
			contjs["flood_routing"]["floodplain_over_channel_fcw"],\
			contjs["flood_routing"]["floodplain_ksat_fpsc"],\
			contjs["geography"]["max_groundwater_storage_gwso"],\
			contjs["geography"]["groundwater_resident_rfto"],\
			contjs["runoff_sim"]["returnflow_ratio_rfpo"],\
			contjs["runoff_sim"]["ksat_adj_sato"],\
			contjs["wind_erosion"]["field_length_fl"],\
			contjs["wind_erosion"]["field_width_fw"],\
			contjs["wind_erosion"]["field_length_angle_ang"]\
			))
		# Line 5
        outfid_cont.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
			contjs["wind_erosion"]["windspeed_distribution_uxp"],\
			contjs["wind_erosion"]["soil_partical_diameter_diam"],\
			contjs["wind_erosion"]["wind_erosion_adj_acw"],\
			contjs["management"]["grazing_limit_gzl0"],\
			contjs["management"]["cultivation_start_year_rtn0"],\
			contjs["weather"]["coef_rainfalldiretow_bxct"],\
			contjs["weather"]["coef_rainfalldirston_byct"],\
			contjs["flood_routing"]["interval_floodrouting_dthy"],\
			contjs["flood_routing"]["routing_threshold_vsc_qth"],\
			contjs["flood_routing"]["vsc_threshold_stnd"]\
			))      
		# Line 6
        outfid_cont.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
			contjs["water_erosion"]["water_erosion_equation_drv"],\
			contjs["geography"]["fraction_ponds_pco0"],\
			contjs["water_erosion"]["usle_c_channel_rcc0"],\
			contjs["nutrient_loss"]["salt_conc_irrig_cslt"],\
			contjs["newpar201911"]["fracinfl_vertcrackpipfl_cpv0"],\
			contjs["newpar201911"]["fracinfl_horizcrackpipfl_cph0"],\
			contjs["newpar201911"]["laythick_diff_soln2gas_dzdn"],\
			contjs["newpar201911"]["time_intervalgasdiff_dtg"],\
			contjs["newpar201911"]["ratio_tp2totalhyd_qpq"]\
			# contjs["water_erosion"]["msi_input_1"],\
			# contjs["water_erosion"]["msi_input_2"],\
			# contjs["water_erosion"]["msi_input_3"],\
			# contjs["water_erosion"]["msi_input_4"]\
			))                                                 
        outfid_cont.close()


    
    def writeOPSCOM(self, jsonwssubsollulatlon, fnopscom):
        """
        This function write OPSCOM files.
        """
        with open(jsonwssubsollulatlon) as json_file:    
            sollulatlong = json.loads(json_file.read())
        json_file.close()

        # Remove file if exists:
        if (os.path.exists(fnopscom)):
            os.remove(fnopscom)

        fidopscom = 0    
        fidopscom = open(fnopscom, "w")
        
        for key, value in sollulatlong.items():
            if 'URBAN' in value["iopsnm"]:
                fidopscom.writelines("%5s\t%s.OPC\n" %(key,
                                              "URBAN"))
            else:
                fidopscom.writelines("%5s\t%s.OPC\n" %(key,
                                              value["iopsnm"]))    

        fidopscom.close()



    def writeAPEXRUN(self, jsonrunsubscen, fnapexrunfl, fnApexProj):
        """
        This function write APEXRUN files.
        """
        with open(jsonrunsubscen) as json_file:    
            subvars = json.loads(json_file.read())
        json_file.close()

        runfid = 0    
        runfid = open(fnapexrunfl, "w")
        
        '''
        1. Run file: runname, sitenumber, monthly wea station no,
        wind weather station no, subarea no, 0 normal soil, 
        subdaily weather file.
        '''

        runWSNames = {}
        
        for wsid in range(len(subvars.keys())):
        # APEXRUN is read with free format in APEX.exe
            runfid.writelines(u"%-10s%7i%7i%7i%7i%7i%7i\n" %(\
                    "RSUB%i_%s" %(wsid+1, fnApexProj) ,\
                            1,\
                            1,\
                            1,\
                            wsid+1,\
                            0, 0\
                            )) 
            runWSNames["ws{}".format(wsid+1)] = "RSUB%i_%s" %(wsid+1, fnApexProj)

        runfid.writelines("%10s%7i%7i%7i%7i%7i%7i\n" %(\
                    "XXXXXXXXXX", 0, 0, 0, 0, 0, 0\
                    ))                    

        runfid.close()

        return runWSNames



    def copyDataBaseFILE(self, fnapexexe, fdApexTio, fdApexData):
        """
        This function copy the database and apex.exe to the run folder.
        """

        filename2copy = {
            "apex1501":fnapexexe,
            "CROPCOM" : "CROPCOM.DAT",
            "TILLCOM" : "TILLCOM.DAT",
            "PEST" : "PESTCOM.DAT",
            "FERTCOM" : "FERTCOM.DAT",
            "TR55COM" : "TR55COM.DAT",
            "PARMS" : "PARMS.DAT",
            "MLRN0806" : "MLRN0806.DAT",
            "APEXDIM" : "APEXDIM.DAT",
            "APEXFILE" : "APEXFILE.DAT",            
            "PRNT0806" : "PRNT0806.DAT",
            "HERD0806" : "HERD0806.DAT",
            #"WDLSTCOM" : "WDLSTCOM.DAT",
            "PSOCOM" : "PSOCOM.DAT",
            "RFDTLST" : "RFDTLST.DAT"
        }

        for key, value in filename2copy.items():

            fndest = None
            fnsrc = None
            fndest = os.path.join(
                fdApexTio,
                value
            )
            fnsrc = os.path.join(
                fdApexData,
                value
            )

            if os.path.exists(fndest):
                os.remove(fndest)

            shutil.copyfile(fnsrc, fndest)


    def runAPEX1501(self, fdApexTio, fdApexProj):
        """
        This function change the directory to the apex run folder,
        run apex, and change back.
        """

        # Change the directory to the apex run folder:
        os.chdir(fdApexTio)
        if globalsetting.osplatform == "linux":
            procCommand = "./%s" %(globalsetting.fnapexbin)                                    
        elif globalsetting.osplatform == "Windows":
            procCommand = "%s" %(globalsetting.fnapexbin)

        generalfuncs.addToLog(procCommand)

        ## call date command ##        
        p = subprocess.run(procCommand, shell=True, stderr=subprocess.PIPE)    
        # Change back to the fdworking folder
        os.chdir(fdApexProj)


    ##########################################################################
    def groupSlope(self, slopepercent):
        
        slopepercent = float(slopepercent)

        if (slopepercent<=0.02):
            slope = 2
        elif ((slopepercent>0.02) and (slopepercent<=0.05)):
            slope = 5
        elif (slopepercent>0.05):
            slope = 10            
            
        return slope


    def createSUBAREALst(self, soilAsc, luAsc, demAsc, sd8Asc,
            blocklat, blocklong):
        
        # Read in asc files
        slpnodata, slopearray = gdalfuncs.readASCMode3(sd8Asc)
        lunodata, landusearray = gdalfuncs.readASCMode3(luAsc)
        solnodata, soilarray = gdalfuncs.readASCMode3(soilAsc)
        demnodata, demarray = gdalfuncs.readASCMode3(demAsc)

        # This is a loop through all arrays.
        # An array will be created to store all
        # of the hru inputs. If the old one is
        # in the list, update the area. If not
        # append one and get area as one.
        # An hru here will have blockid, 
        # soil, landuse, slope. 
        # will be used for getting soil from
        # the database.
        subarealist = {}

        for rowidx in range(1, len(landusearray)-1):
            for colidx in range(1, len(landusearray[rowidx])-1):
                    
                # A temparaary container to store an subarea info
                tempsubarea = []
                # If not no data cells,
                if ((soilarray[rowidx][colidx] != solnodata)
                    and (landusearray[rowidx][colidx] != lunodata)
                    and (slopearray[rowidx][colidx] != slpnodata)):
                    
                    tempsubarea = [soilarray[rowidx][colidx],
                                landusearray[rowidx][colidx],
                                str(self.groupSlope(
                                    slopearray[rowidx][colidx]))
                                ]

                    tempsubarea = "_".join(tempsubarea)
                    if not tempsubarea in subarealist: 
                        # [area, slope, elev, latitude, longitude]
                        subarealist[tempsubarea] = [1, 
                                [float(slopearray[rowidx][colidx])],
                                [float(demarray[rowidx][colidx])],
                                blocklat, blocklong, 
                                soilarray[rowidx][colidx],
                                landusearray[rowidx][colidx],
                                int(self.groupSlope(
                                    slopearray[rowidx][colidx]))
                                ]
                    else:
                        subarealist[tempsubarea][0] = subarealist[tempsubarea][0] + 1
                        subarealist[tempsubarea][1].append(float(slopearray[rowidx][colidx]))
                        subarealist[tempsubarea][2].append(float(demarray[rowidx][colidx]))
        # Calculate average slope and elevation
        # Here we will use one latitude and longitude for one block, 
        # so they will not be changed.
        for key, value in subarealist.items():
            value[1] = sum(value[1])/len(value[1])
            value[2] = sum(value[2])/len(value[2])
                    
        
        return subarealist

