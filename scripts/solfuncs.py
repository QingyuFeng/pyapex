# -*- coding: utf-8 -*-

import os
import json
import pandas as pd
import sqlite3


class solfuncs():
    """Various utilities."""

    @staticmethod
    def writejson2sol(usr_runfd, soljs):
        # I will use a distionary for cont lines
        # It will be initiated first as the template for stop.
        solf_name = ''
    
        # Test whether new there is soil test n and P
        solf_name = "SOL%s.SOL" %(soljs["solmukey"]) 

        # Start writing sol files    
        wfid_sol = 0
        wfid_sol = open(r"%s/%s" %(usr_runfd, solf_name) , "w")
    
        # Write line 1: desctiption
        sol_l1 = 0
        sol_l1 = "%20s\n" %(soljs["line1"]["soilname"])
        wfid_sol.writelines(sol_l1)
    
        # Writing line 2
        sol_l2 = 0
        #    ! SOIL PROPERTIES
    
        # modify hydrologic soi group from ABCD  to `1234' AS REQUIRED IN APEX.

        if "/" in soljs["line2"]["hydrologicgroup_hsg"]:
            soljs["line2"]["hydrologicgroup_hsg"]=\
                soljs["line2"]["hydrologicgroup_hsg"].split("/")[0]
    
        if soljs["line2"]["hydrologicgroup_hsg"] == "A":
            soljs["line2"]["hydrologicgroup_hsg"] = "1"
        elif soljs["line2"]["hydrologicgroup_hsg"] == "B":
            soljs["line2"]["hydrologicgroup_hsg"] = "2"
        elif soljs["line2"]["hydrologicgroup_hsg"] == "C":
            soljs["line2"]["hydrologicgroup_hsg"] = "3"        
        else:
            soljs["line2"]["hydrologicgroup_hsg"] = "4"
    
        sol_l2 = "%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n"\
                        %(float(soljs["line2"]["abledo_salb"]),\
                          float(soljs["line2"]["hydrologicgroup_hsg"]), \
                          float(soljs["line2"]["initialwatercontent_ffc"]),\
                          0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00)
        wfid_sol.writelines(sol_l2)
    
        # Line 3:  Same format as line 2, different parameters. 
        # Some values were set to prevent any potential model run failure.
        # the 5th variable ZQT, should be from 0.01 to 0.25.
        # the 6th and 7th variable ZF should be from 0.05 to 0.25
        # the 8 and 9 should be larger than 0.03 and 0.3
        # The 10th should be left blank
        sol_l3 = 0
        sol_l3 = "%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f        \n"\
                    %(float(soljs["line3"]["min_layerdepth_tsla"]), 
                        float(soljs["line3"]["weatheringcode_xids"]),
                        float(soljs["line3"]["cultivationyears_rtn1"]),
                        float(soljs["line3"]["grouping_xidk"]),
                        float(soljs["line3"]["min_maxlayerthick_zqt"]),
                        float(soljs["line3"]["minprofilethick_zf"]),
                        float(soljs["line3"]["minlayerthick_ztk"]),
                        float(soljs["line3"]["org_c_biomass_fbm"]),
                        float(soljs["line3"]["org_c_passive_fhp"])
                        )
        wfid_sol.writelines(sol_l3)
    
        # Starting from line 4, the variables will be writen for 
        # properties for eacy layer, and each column represent one layer.
        # It is better to use a loop to do the writing.
    
        sol_layer_pro = [""]*52
        layeridxlst = [int(float(soljs["layerid"]["z1"])),
                       int(float(soljs["layerid"]["z2"])),
                        int(float(soljs["layerid"]["z3"])),
                        int(float(soljs["layerid"]["z4"])),
                        int(float(soljs["layerid"]["z5"])),
                        int(float(soljs["layerid"]["z6"])),
                        int(float(soljs["layerid"]["z7"])),
                        int(float(soljs["layerid"]["z8"])),
                        int(float(soljs["layerid"]["z9"])),
                        int(float(soljs["layerid"]["z10"]))
                        ]
        
        for layeridx in range(0, max(layeridxlst)):
            if layeridx < max(layeridxlst)-1:
                #print(layeridx)
        #  !  4  Z    = DEPTH TO BOTTOM OF LAYERS(m)            
                sol_layer_pro[3] = sol_layer_pro[3] + "%8.2f" \
                    %(float(soljs["line4_layerdepth"]["z%i" %(layeridx+1)]))
    #  !  5  BD   = BULK DENSITY(t/m3)                
                sol_layer_pro[4] = sol_layer_pro[4] + "%8.2f" \
                    %(float(soljs["line5_moistbulkdensity"]["z%i" %(layeridx+1)]))
    #  !  6  UW   = SOIL WATER CONTENT AT WILTING POINT(1500 KPA)(m/m)                                             
    #  !            (BLANK IF UNKNOWN)                
                sol_layer_pro[5] = sol_layer_pro[5] + "%8.2f" \
                    %(float(soljs["line6_wiltingpoint"]["z%i" %(layeridx+1)])/100)
    #  !  7  FC   = WATER CONTENT AT FIELD CAPACITY(33KPA)(m/m)                                                    
    #  !            (BLANK IF UNKNOWN)                
                sol_layer_pro[6] = sol_layer_pro[6] + "%8.2f" \
                    %(float(soljs["line7_fieldcapacity"]["z%i" %(layeridx+1)])/100)
    #  !  8  SAN  = % SAND                 
                sol_layer_pro[7] = sol_layer_pro[7] + "%8.2f" \
                    %(float(soljs["line8_sand"]["z%i" %(layeridx+1)]))
    #  !  9  SIL  = % SILT                
                sol_layer_pro[8] = sol_layer_pro[8] + "%8.2f" \
                    %(float(soljs["line9_silt"]["z%i" %(layeridx+1)]))
    #  ! 10  WN   = INITIAL ORGANIC N CONC(g/t)       (BLANK IF UNKNOWN)                
                sol_layer_pro[9] = sol_layer_pro[9] + "%8.2f" \
                    %(0.00)
    #  ! 11  PH   = SOIL PH                
                sol_layer_pro[10] = sol_layer_pro[10] + "%8.2f" \
                    %(float(soljs["line11_ph"]["z%i" %(layeridx+1)]))
    #  ! 12  SMB  = SUM OF BASES(cmol/kg)              (BLANK IF UNKNOWN)
                sol_layer_pro[11] = sol_layer_pro[11] + "%8.2f" \
                    %(float(soljs["line12_sumofbase_smb"]["z%i" %(layeridx+1)]))
    #  ! 13  WOC  = ORGANIC CARBON CONC(%)                
                sol_layer_pro[12] = sol_layer_pro[12] + "%8.2f" \
                    %(float(soljs["line13_orgc_conc_woc"]["z%i" %(layeridx+1)]))
    #  ! 14  CAC  = CALCIUM CARBONATE(%)                 
                sol_layer_pro[13] = sol_layer_pro[13] + "%8.2f" \
                    %(float(soljs["line14_caco3_cac"]["z%i" %(layeridx+1)]))
    #  ! 15  CEC  = CATION EXCHANGE CAPACITY(cmol/kg)(BLANK IF UNKNOWN                
                sol_layer_pro[14] = sol_layer_pro[14] + "%8.2f" \
                    %(float(soljs["line15_cec"]["z%i" %(layeridx+1)]))
    #  ! 16  ROK  = COARSE FRAGMENTS(% VOL)              (BLANK IF UNKNOWN)           
                sol_layer_pro[15] = sol_layer_pro[15] + "%8.2f" \
                    %(float(soljs["line16_rock_rok"]["z%i" %(layeridx+1)]))
    #  ! 17  CNDS = INITIAL SOL N CONC(g/t)            (BLANK IF UNKNOWN) 
                sol_layer_pro[16] = sol_layer_pro[16] + "%8.2f" \
                    %(float(soljs["line17_inisolnconc_cnds"]["z%i" %(layeridx+1)]))
    #  ! 18  SSF  = INITIAL SOL P CONC(g/t)       (BLANK IF UNKNOWN)
                sol_layer_pro[17] = sol_layer_pro[17] + "%8.2f" \
                    %(0.00)
    #  ! 19  RSD  = CROP RESIDUE(t/ha)                (BLANK IF UNKNOWN)   
                sol_layer_pro[18] = sol_layer_pro[18] + "%8.2f" \
                    %(0.00)
    #  ! 20  BDD  = BULK DENSITY(OVEN DRY)(t/m3)   (BLANK IF UNKNOWN)                
                sol_layer_pro[19] = sol_layer_pro[19] + "%8.2f" \
                    %(float(soljs["line20_drybd_bdd"]["z%i" %(layeridx+1)]))
    #  ! 21  PSP  = P SORPTION RATIO                   (BLANK IF UNKNOWN)                  
                sol_layer_pro[20] = sol_layer_pro[20] + "%8.2f" \
                    %(0.00) 
    #  ! 22  SATC = SATURATED CONDUCTIVITY(mm/h)     (BLANK IF UNKNOWN)
                sol_layer_pro[21] = sol_layer_pro[21] + "%8.2f" \
                    %(float(soljs["line22_ksat"]["z%i" %(layeridx+1)]))
    #  ! 23  HCL  = LATERAL HYDRAULIC CONDUCTIVITY(mm/h)                
                sol_layer_pro[22] = sol_layer_pro[22] + "%8.2f" \
                    %(float(soljs["line22_ksat"]["z%i" %(layeridx+1)])/2)
    #  ! 24  WPO  = INITIAL ORGANIC P CONC(g/t)      (BLANK IF UNKNOWN)                
                sol_layer_pro[23] = sol_layer_pro[23] + "%8.2f" \
                    %(float(soljs["line24_orgp_wpo"]["z%i" %(layeridx+1)]))
    #  ! 25  DHN  = EXCHANGEABLE K CONC (g/t)                
                sol_layer_pro[24] = sol_layer_pro[24] + "%8.2f" \
                    %(0.00)
    #  ! 26  ECND = ELECTRICAL COND (mmho/cm)                
                sol_layer_pro[25] = sol_layer_pro[25] + "%8.2f" \
                    %(float(soljs["line26_electricalcond_ec"]["z%i" %(layeridx+1)]))
    #  ! 27  STFR = FRACTION OF STORAGE INTERACTING WITH NO3 LEACHING                                              
    #  !                                               (BLANK IF UNKNOWN)                
                sol_layer_pro[26] = sol_layer_pro[26] + "%8.2f" \
                    %(0.00)
    #  ! 28  SWST = INITIAL SOIL WATER STORAGE (m/m)                
                sol_layer_pro[27] = sol_layer_pro[27] + "%8.2f" \
                    %(0.00)
    #  ! 29  CPRV = FRACTION INFLOW PARTITIONED TO VERTICLE CRACK OR PIPE FLOW                
                sol_layer_pro[28] = sol_layer_pro[28] + "%8.2f" \
                    %(0.00)
    #  ! 30  CPRH = FRACTION INFLOW PARTITIONED TO HORIZONTAL CRACK OR PIPE                                        
    #  !            FLOW                 
                sol_layer_pro[29] = sol_layer_pro[29] + "%8.2f" \
                    %(0.00)
    #  ! 31  WLS  = STRUCTURAL LITTER(kg/ha)           (BLANK IF UNKNOWN)                
                sol_layer_pro[30] = sol_layer_pro[30] + "%8.2f" \
                    %(0.00)
    #  ! 32  WLM  = METABOLIC LITTER(kg/ha)            (BLANK IF UNKNOWN)            
                sol_layer_pro[31] = sol_layer_pro[31] + "%8.2f" \
                    %(0.00)
    #  ! 33  WLSL = LIGNIN CONTENT OF STRUCTURAL LITTER(kg/ha)(B I U)                
                sol_layer_pro[32] = sol_layer_pro[32] + "%8.2f" \
                    %(0.00)
    #  ! 34  WLSC = CARBON CONTENT OF STRUCTURAL LITTER(kg/ha)(B I U) 
                sol_layer_pro[33] = sol_layer_pro[33] + "%8.2f" \
                    %(0.00)
    #  ! 35  WLMC = C CONTENT OF METABOLIC LITTER(kg/ha)(B I U)
                sol_layer_pro[34] = sol_layer_pro[34] + "%8.2f" \
                    %(0.00)
    #  ! 36  WLSLC= C CONTENT OF LIGNIN OF STRUCTURAL LITTER(kg/ha)(B I U)
                sol_layer_pro[35] = sol_layer_pro[35] + "%8.2f" \
                    %(0.00)
    #  ! 37  WLSLNC=N CONTENT OF LIGNIN OF STRUCTURAL LITTER(kg/ha)(BIU)
                sol_layer_pro[36] = sol_layer_pro[36] + "%8.2f" \
                    %(0.00)
    #  ! 38  WBMC = C CONTENT OF BIOMASS(kg/ha)(BIU)
                sol_layer_pro[37] = sol_layer_pro[37] + "%8.2f" \
                    %(0.00)
    #  ! 39  WHSC = C CONTENT OF SLOW HUMUS(kg/ha)(BIU)
                sol_layer_pro[38] = sol_layer_pro[38] + "%8.2f" \
                    %(0.00)
    #  ! 40  WHPC = C CONTENT OF PASSIVE HUMUS(kg/ha)(BIU)
                sol_layer_pro[39] = sol_layer_pro[39] + "%8.2f" \
                    %(0.00)
    #  ! 41  WLSN = N CONTENT OF STRUCTURAL LITTER(kg/ha)(BIU)
                sol_layer_pro[40] = sol_layer_pro[40] + "%8.2f" \
                    %(0.00)
    #  ! 42  WLMN = N CONTENT OF METABOLIC LITTER(kg/ha)(BIU)
                sol_layer_pro[41] = sol_layer_pro[41] + "%8.2f" \
                    %(0.00)
    #  ! 43  WBMN = N CONTENT OF BIOMASS(kg/ha)(BIU)
                sol_layer_pro[42] = sol_layer_pro[42] + "%8.2f" \
                    %(0.00)
    #  ! 44  WHSN = N CONTENT OF SLOW HUMUS(kg/ha)(BIU)
                sol_layer_pro[43] = sol_layer_pro[43] + "%8.2f" \
                    %(0.00)
    #  ! 45  WHPN = N CONTENT OF PASSIVE HUMUS(kg/ha)(BIU)
                sol_layer_pro[44] = sol_layer_pro[44] + "%8.2f" \
                    %(0.00)
    #  ! 46  FE26 = IRON CONTENT(%)
                sol_layer_pro[45] = sol_layer_pro[45] + "%8.2f" \
                    %(0.00)
    #  ! 47  SULF = SULFUR CONTENT(%)                 
                sol_layer_pro[46] = sol_layer_pro[46] + "%8.2f" \
                    %(0.00)
    #  ! 48  ASHZ = SOIL HORIZON(A,B,C)                                                                            
                sol_layer_pro[47] = sol_layer_pro[47] + "%8s" \
                    %(" ")
    #   ! 49  CGO2 = O2 CONC IN GAS PHASE (g/m3 OF SOIL AIR)
                sol_layer_pro[48] = sol_layer_pro[48] + "%8.2f" \
                    %(0.00)
    #   ! 50  CGCO2= CO2 CONC IN GAS PHASE (g/m3 OF SOIL AIR)                                                       
                sol_layer_pro[49] = sol_layer_pro[49] + "%8.2f" \
                    %(0.00)
    #   ! 51  CGN2O= N2O CONC IN GAS PHASE (g/m3 OF SOIL AIR)                 
                sol_layer_pro[50] = sol_layer_pro[50] + "%8.2f" \
                    %(0.00)
            else:
        #  !  4  Z    = DEPTH TO BOTTOM OF LAYERS(m)            
                sol_layer_pro[3] = sol_layer_pro[3] + "%8.2f\n" \
                    %(float(soljs["line4_layerdepth"]["z%i" %(layeridx+1)]))
    #  !  5  BD   = BULK DENSITY(t/m3)                
                sol_layer_pro[4] = sol_layer_pro[4] + "%8.2f\n" \
                    %(float(soljs["line5_moistbulkdensity"]["z%i" %(layeridx+1)]))
    #  !  6  UW   = SOIL WATER CONTENT AT WILTING POINT(1500 KPA)(m/m)                                             
    #  !            (BLANK IF UNKNOWN)                
                sol_layer_pro[5] = sol_layer_pro[5] + "%8.2f\n" \
                    %(float(soljs["line6_wiltingpoint"]["z%i" %(layeridx+1)])/100)
    #  !  7  FC   = WATER CONTENT AT FIELD CAPACITY(33KPA)(m/m)                                                    
    #  !            (BLANK IF UNKNOWN)                
                sol_layer_pro[6] = sol_layer_pro[6] + "%8.2f\n" \
                    %(float(soljs["line7_fieldcapacity"]["z%i" %(layeridx+1)])/100)
    #  !  8  SAN  = % SAND                 
                sol_layer_pro[7] = sol_layer_pro[7] + "%8.2f\n" \
                    %(float(soljs["line8_sand"]["z%i" %(layeridx+1)]))
    #  !  9  SIL  = % SILT                
                sol_layer_pro[8] = sol_layer_pro[8] + "%8.2f\n" \
                    %(float(soljs["line9_silt"]["z%i" %(layeridx+1)]))
    #  ! 10  WN   = INITIAL ORGANIC N CONC(g/t)       (BLANK IF UNKNOWN)                
                sol_layer_pro[9] = sol_layer_pro[9] + "%8.2f\n" \
                    %(0.00)
    #  ! 11  PH   = SOIL PH                
                sol_layer_pro[10] = sol_layer_pro[10] + "%8.2f\n" \
                    %(float(soljs["line11_ph"]["z%i" %(layeridx+1)]))
    #  ! 12  SMB  = SUM OF BASES(cmol/kg)              (BLANK IF UNKNOWN)
                sol_layer_pro[11] = sol_layer_pro[11] + "%8.2f\n" \
                    %(float(soljs["line12_sumofbase_smb"]["z%i" %(layeridx+1)]))
    #  ! 13  WOC  = ORGANIC CARBON CONC(%)                
                sol_layer_pro[12] = sol_layer_pro[12] + "%8.2f\n" \
                    %(float(soljs["line13_orgc_conc_woc"]["z%i" %(layeridx+1)]))
    #  ! 14  CAC  = CALCIUM CARBONATE(%)                 
                sol_layer_pro[13] = sol_layer_pro[13] + "%8.2f\n" \
                    %(float(soljs["line14_caco3_cac"]["z%i" %(layeridx+1)]))
    #  ! 15  CEC  = CATION EXCHANGE CAPACITY(cmol/kg)(BLANK IF UNKNOWN                
                sol_layer_pro[14] = sol_layer_pro[14] + "%8.2f\n" \
                    %(float(soljs["line15_cec"]["z%i" %(layeridx+1)]))
    #  ! 16  ROK  = COARSE FRAGMENTS(% VOL)              (BLANK IF UNKNOWN)           
                sol_layer_pro[15] = sol_layer_pro[15] + "%8.2f\n" \
                    %(float(soljs["line16_rock_rok"]["z%i" %(layeridx+1)]))
    #  ! 17  CNDS = INITIAL SOL N CONC(g/t)            (BLANK IF UNKNOWN) 
                sol_layer_pro[16] = sol_layer_pro[16] + "%8.2f\n" \
                    %(float(soljs["line17_inisolnconc_cnds"]["z%i" %(layeridx+1)]))
    #  ! 18  SSF  = INITIAL SOL P CONC(g/t)       (BLANK IF UNKNOWN)
                sol_layer_pro[17] = sol_layer_pro[17] + "%8.2f\n" \
                    %(0.00)
    #  ! 19  RSD  = CROP RESIDUE(t/ha)                (BLANK IF UNKNOWN)   
                sol_layer_pro[18] = sol_layer_pro[18] + "%8.2f\n" \
                    %(0.00)
    #  ! 20  BDD  = BULK DENSITY(OVEN DRY)(t/m3)   (BLANK IF UNKNOWN)                
                sol_layer_pro[19] = sol_layer_pro[19] + "%8.2f\n" \
                    %(float(soljs["line20_drybd_bdd"]["z%i" %(layeridx+1)]))
    #  ! 21  PSP  = P SORPTION RATIO                   (BLANK IF UNKNOWN)                  
                sol_layer_pro[20] = sol_layer_pro[20] + "%8.2f\n" \
                    %(0.00) 
    #  ! 22  SATC = SATURATED CONDUCTIVITY(mm/h)     (BLANK IF UNKNOWN)
                sol_layer_pro[21] = sol_layer_pro[21] + "%8.2f\n" \
                    %(float(soljs["line22_ksat"]["z%i" %(layeridx+1)]))
    #  ! 23  HCL  = LATERAL HYDRAULIC CONDUCTIVITY(mm/h)                
                sol_layer_pro[22] = sol_layer_pro[22] + "%8.2f\n" \
                    %(float(soljs["line22_ksat"]["z%i" %(layeridx+1)])/2)
    #  ! 24  WPO  = INITIAL ORGANIC P CONC(g/t)      (BLANK IF UNKNOWN)                
                sol_layer_pro[23] = sol_layer_pro[23] + "%8.2f\n" \
                    %(float(soljs["line24_orgp_wpo"]["z%i" %(layeridx+1)]))
    #  ! 25  DHN  = EXCHANGEABLE K CONC (g/t)                
                sol_layer_pro[24] = sol_layer_pro[24] + "%8.2f\n" \
                    %(0.00)
    #  ! 26  ECND = ELECTRICAL COND (mmho/cm)                
                sol_layer_pro[25] = sol_layer_pro[25] + "%8.2f\n" \
                    %(float(soljs["line26_electricalcond_ec"]["z%i" %(layeridx+1)]))
    #  ! 27  STFR = FRACTION OF STORAGE INTERACTING WITH NO3 LEACHING                                              
    #  !                                               (BLANK IF UNKNOWN)                
                sol_layer_pro[26] = sol_layer_pro[26] + "%8.2f\n" \
                    %(0.00)
    #  ! 28  SWST = INITIAL SOIL WATER STORAGE (m/m)                
                sol_layer_pro[27] = sol_layer_pro[27] + "%8.2f\n" \
                    %(0.00)
    #  ! 29  CPRV = FRACTION INFLOW PARTITIONED TO VERTICLE CRACK OR PIPE FLOW                
                sol_layer_pro[28] = sol_layer_pro[28] + "%8.2f\n" \
                    %(0.00)
    #  ! 30  CPRH = FRACTION INFLOW PARTITIONED TO HORIZONTAL CRACK OR PIPE                                        
    #  !            FLOW                 
                sol_layer_pro[29] = sol_layer_pro[29] + "%8.2f\n" \
                    %(0.00)
    #  ! 31  WLS  = STRUCTURAL LITTER(kg/ha)           (BLANK IF UNKNOWN)                
                sol_layer_pro[30] = sol_layer_pro[30] + "%8.2f\n" \
                    %(0.00)
    #  ! 32  WLM  = METABOLIC LITTER(kg/ha)            (BLANK IF UNKNOWN)            
                sol_layer_pro[31] = sol_layer_pro[31] + "%8.2f\n" \
                    %(0.00)
    #  ! 33  WLSL = LIGNIN CONTENT OF STRUCTURAL LITTER(kg/ha)(B I U)                
                sol_layer_pro[32] = sol_layer_pro[32] + "%8.2f\n" \
                    %(0.00)
    #  ! 34  WLSC = CARBON CONTENT OF STRUCTURAL LITTER(kg/ha)(B I U) 
                sol_layer_pro[33] = sol_layer_pro[33] + "%8.2f\n" \
                    %(0.00)
    #  ! 35  WLMC = C CONTENT OF METABOLIC LITTER(kg/ha)(B I U)
                sol_layer_pro[34] = sol_layer_pro[34] + "%8.2f\n" \
                    %(0.00)
    #  ! 36  WLSLC= C CONTENT OF LIGNIN OF STRUCTURAL LITTER(kg/ha)(B I U)
                sol_layer_pro[35] = sol_layer_pro[35] + "%8.2f\n" \
                    %(0.00)
    #  ! 37  WLSLNC=N CONTENT OF LIGNIN OF STRUCTURAL LITTER(kg/ha)(BIU)
                sol_layer_pro[36] = sol_layer_pro[36] + "%8.2f\n" \
                    %(0.00)
    #  ! 38  WBMC = C CONTENT OF BIOMASS(kg/ha)(BIU)
                sol_layer_pro[37] = sol_layer_pro[37] + "%8.2f\n" \
                    %(0.00)
    #  ! 39  WHSC = C CONTENT OF SLOW HUMUS(kg/ha)(BIU)
                sol_layer_pro[38] = sol_layer_pro[38] + "%8.2f\n" \
                    %(0.00)
    #  ! 40  WHPC = C CONTENT OF PASSIVE HUMUS(kg/ha)(BIU)
                sol_layer_pro[39] = sol_layer_pro[39] + "%8.2f\n" \
                    %(0.00)
    #  ! 41  WLSN = N CONTENT OF STRUCTURAL LITTER(kg/ha)(BIU)
                sol_layer_pro[40] = sol_layer_pro[40] + "%8.2f\n" \
                    %(0.00)
    #  ! 42  WLMN = N CONTENT OF METABOLIC LITTER(kg/ha)(BIU)
                sol_layer_pro[41] = sol_layer_pro[41] + "%8.2f\n" \
                    %(0.00)
    #  ! 43  WBMN = N CONTENT OF BIOMASS(kg/ha)(BIU)
                sol_layer_pro[42] = sol_layer_pro[42] + "%8.2f\n" \
                    %(0.00)
    #  ! 44  WHSN = N CONTENT OF SLOW HUMUS(kg/ha)(BIU)
                sol_layer_pro[43] = sol_layer_pro[43] + "%8.2f\n" \
                    %(0.00)
    #  ! 45  WHPN = N CONTENT OF PASSIVE HUMUS(kg/ha)(BIU)
                sol_layer_pro[44] = sol_layer_pro[44] + "%8.2f\n" \
                    %(0.00)
    #  ! 46  FE26 = IRON CONTENT(%)
                sol_layer_pro[45] = sol_layer_pro[45] + "%8.2f\n" \
                    %(0.00)
    #  ! 47  SULF = SULFUR CONTENT(%)                 
                sol_layer_pro[46] = sol_layer_pro[46] + "%8.2f\n" \
                    %(0.00)
    #  ! 48  ASHZ = SOIL HORIZON(A,B,C)                                                                            
                sol_layer_pro[47] = sol_layer_pro[47] + "%8s\n" \
                    %(" ")
    #   ! 49  CGO2 = O2 CONC IN GAS PHASE (g/m3 OF SOIL AIR)
                sol_layer_pro[48] = sol_layer_pro[48] + "%8.2f\n" \
                    %(0.00)
    #   ! 50  CGCO2= CO2 CONC IN GAS PHASE (g/m3 OF SOIL AIR)                                                       
                sol_layer_pro[49] = sol_layer_pro[49] + "%8.2f\n" \
                    %(0.00)
    #   ! 51  CGN2O= N2O CONC IN GAS PHASE (g/m3 OF SOIL AIR)                 
                sol_layer_pro[50] = sol_layer_pro[50] + "%8.2f\n" \
                    %(0.00)
    
        for layproidx in range(3, 51):
            wfid_sol.writelines(sol_layer_pro[layproidx])
    
        
        wfid_sol.close()



    @staticmethod
    def update1soljson(fnDbSoil: str,
                    solmk: str, 
                    solmkreal: str,
                    jsonupdate_sol: str,
                    fnTbSoil: str):
        
        sqlconn = None
        try:
            sqlconn = sqlite3.connect(fnDbSoil)
        except sqlite3.Error as e:
            print(e)

        jsonupdate_sol[solmk]["solmukey"]= solmkreal
        sqlstmt = "SELECT * FROM %s where mukey = %s order by mukey" %(
                                    fnTbSoil,
                                    solmkreal)

        Result = pd.read_sql(sqlstmt, con=sqlconn)

        if sqlconn is not None:
            sqlconn.close()

        jsonupdate_sol[solmk]["line1"]["soilname"] = str(Result.loc[0, "muname"])
        jsonupdate_sol[solmk]["line2"]["abledo_salb"]= "0.03"
        jsonupdate_sol[solmk]["line2"]["hydrologicgroup_hsg"]= str(Result.loc[0, "hydgrpdcd"])
        jsonupdate_sol[solmk]["line2"]["initialwatercontent_ffc"]= "0.00"
        jsonupdate_sol[solmk]["line2"]["minwatertabledep_wtmn"]= "0.00"
        jsonupdate_sol[solmk]["line2"]["maxwatertabledep_wtmx"]= "0.00"
        jsonupdate_sol[solmk]["line2"]["initialwatertable_wtbl"]= "0.00"
        jsonupdate_sol[solmk]["line2"]["groundwaterstorage_gwst"]= "0.00"
        jsonupdate_sol[solmk]["line2"]["max_groundwater_gwmx"]= "0.00"
        jsonupdate_sol[solmk]["line2"]["gw_residenttime_rftt"]= "0.00"
        jsonupdate_sol[solmk]["line2"]["return_overtotalflow_rfpk"] = "0.00"

        jsonupdate_sol[solmk]["line3"]["min_layerdepth_tsla"]= "10.00"
        jsonupdate_sol[solmk]["line3"]["weatheringcode_xids"]= "0.00"
        jsonupdate_sol[solmk]["line3"]["cultivationyears_rtn1"]= "50.00"
        jsonupdate_sol[solmk]["line3"]["grouping_xidk"]= "2.00"
        jsonupdate_sol[solmk]["line3"]["min_maxlayerthick_zqt"]= "0.00"
        jsonupdate_sol[solmk]["line3"]["minprofilethick_zf"]= "0.00"
        jsonupdate_sol[solmk]["line3"]["minlayerthick_ztk"]= "0.00"
        jsonupdate_sol[solmk]["line3"]["org_c_biomass_fbm"]= "0.00"
        jsonupdate_sol[solmk]["line3"]["org_c_passive_fhp"]= "0.00"

        jsonupdate_sol[solmk]["line4_layerdepth"]["z1"]= str(Result.loc[0, "L1_layerdepth"])
        jsonupdate_sol[solmk]["line4_layerdepth"]["z2"]= str(Result.loc[0, "L2_layerdepth"])
        jsonupdate_sol[solmk]["line4_layerdepth"]["z3"]= str(Result.loc[0, "L3_layerdepth"])
        jsonupdate_sol[solmk]["line4_layerdepth"]["z4"]= str(Result.loc[0, "L4_layerdepth"])
        jsonupdate_sol[solmk]["line4_layerdepth"]["z5"]= str(Result.loc[0, "L5_layerdepth"])
        jsonupdate_sol[solmk]["line4_layerdepth"]["z6"]= str(Result.loc[0, "L6_layerdepth"])
        jsonupdate_sol[solmk]["line4_layerdepth"]["z7"]= str(Result.loc[0, "L7_layerdepth"])
        jsonupdate_sol[solmk]["line4_layerdepth"]["z8"]= str(Result.loc[0, "L8_layerdepth"])
        jsonupdate_sol[solmk]["line4_layerdepth"]["z9"]= str(Result.loc[0, "L9_layerdepth"])
        jsonupdate_sol[solmk]["line4_layerdepth"]["z10"]= str(Result.loc[0, "L10_layerdepth"])

        jsonupdate_sol[solmk]["line5_moistbulkdensity"]["z1"]= str(Result.loc[0, "L1_BulkDensity"])
        jsonupdate_sol[solmk]["line5_moistbulkdensity"]["z2"]= str(Result.loc[0, "L2_BulkDensity"])
        jsonupdate_sol[solmk]["line5_moistbulkdensity"]["z3"]= str(Result.loc[0, "L3_BulkDensity"])
        jsonupdate_sol[solmk]["line5_moistbulkdensity"]["z4"]= str(Result.loc[0, "L4_BulkDensity"])
        jsonupdate_sol[solmk]["line5_moistbulkdensity"]["z5"]= str(Result.loc[0, "L5_BulkDensity"])
        jsonupdate_sol[solmk]["line5_moistbulkdensity"]["z6"]= str(Result.loc[0, "L6_BulkDensity"])
        jsonupdate_sol[solmk]["line5_moistbulkdensity"]["z7"]= str(Result.loc[0, "L7_BulkDensity"])
        jsonupdate_sol[solmk]["line5_moistbulkdensity"]["z8"]= str(Result.loc[0, "L8_BulkDensity"])
        jsonupdate_sol[solmk]["line5_moistbulkdensity"]["z9"]= str(Result.loc[0, "L9_BulkDensity"])
        jsonupdate_sol[solmk]["line5_moistbulkdensity"]["z10"]= str(Result.loc[0, "L10_BulkDensity"])

        jsonupdate_sol[solmk]["line6_wiltingpoint"]["z1"]= str(Result.loc[0, "L1_WiltingPoint"])
        jsonupdate_sol[solmk]["line6_wiltingpoint"]["z2"]= str(Result.loc[0, "L2_WiltingPoint"])
        jsonupdate_sol[solmk]["line6_wiltingpoint"]["z3"]= str(Result.loc[0, "L3_WiltingPoint"])
        jsonupdate_sol[solmk]["line6_wiltingpoint"]["z4"]= str(Result.loc[0, "L4_WiltingPoint"])
        jsonupdate_sol[solmk]["line6_wiltingpoint"]["z5"]= str(Result.loc[0, "L5_WiltingPoint"])
        jsonupdate_sol[solmk]["line6_wiltingpoint"]["z6"]= str(Result.loc[0, "L6_WiltingPoint"])
        jsonupdate_sol[solmk]["line6_wiltingpoint"]["z7"]= str(Result.loc[0, "L7_WiltingPoint"])
        jsonupdate_sol[solmk]["line6_wiltingpoint"]["z8"]= str(Result.loc[0, "L8_WiltingPoint"])
        jsonupdate_sol[solmk]["line6_wiltingpoint"]["z9"]= str(Result.loc[0, "L9_WiltingPoint"])
        jsonupdate_sol[solmk]["line6_wiltingpoint"]["z10"]= str(Result.loc[0, "L10_WiltingPoint"])

        jsonupdate_sol[solmk]["line7_fieldcapacity"]["z1"]= str(Result.loc[0, "L1_FieldCapacity"])
        jsonupdate_sol[solmk]["line7_fieldcapacity"]["z2"]= str(Result.loc[0, "L2_FieldCapacity"])
        jsonupdate_sol[solmk]["line7_fieldcapacity"]["z3"]= str(Result.loc[0, "L3_FieldCapacity"])
        jsonupdate_sol[solmk]["line7_fieldcapacity"]["z4"]= str(Result.loc[0, "L4_FieldCapacity"])
        jsonupdate_sol[solmk]["line7_fieldcapacity"]["z5"]= str(Result.loc[0, "L5_FieldCapacity"])
        jsonupdate_sol[solmk]["line7_fieldcapacity"]["z6"]= str(Result.loc[0, "L6_FieldCapacity"])
        jsonupdate_sol[solmk]["line7_fieldcapacity"]["z7"]= str(Result.loc[0, "L7_FieldCapacity"])
        jsonupdate_sol[solmk]["line7_fieldcapacity"]["z8"]= str(Result.loc[0, "L8_FieldCapacity"])
        jsonupdate_sol[solmk]["line7_fieldcapacity"]["z9"]= str(Result.loc[0, "L9_FieldCapacity"])
        jsonupdate_sol[solmk]["line7_fieldcapacity"]["z10"]= str(Result.loc[0, "L10_FieldCapacity"])

        jsonupdate_sol[solmk]["line8_sand"]["z1"]= str(Result.loc[0, "L1_SandTotal"])
        jsonupdate_sol[solmk]["line8_sand"]["z2"]= str(Result.loc[0, "L2_SandTotal"])
        jsonupdate_sol[solmk]["line8_sand"]["z3"]= str(Result.loc[0, "L3_SandTotal"])
        jsonupdate_sol[solmk]["line8_sand"]["z4"]= str(Result.loc[0, "L4_SandTotal"])
        jsonupdate_sol[solmk]["line8_sand"]["z5"]= str(Result.loc[0, "L5_SandTotal"])
        jsonupdate_sol[solmk]["line8_sand"]["z6"]= str(Result.loc[0, "L6_SandTotal"])
        jsonupdate_sol[solmk]["line8_sand"]["z7"]= str(Result.loc[0, "L7_SandTotal"])
        jsonupdate_sol[solmk]["line8_sand"]["z8"]= str(Result.loc[0, "L8_SandTotal"])
        jsonupdate_sol[solmk]["line8_sand"]["z9"]= str(Result.loc[0, "L9_SandTotal"])
        jsonupdate_sol[solmk]["line8_sand"]["z10"]= str(Result.loc[0, "L10_SandTotal"])

        jsonupdate_sol[solmk]["line9_silt"]["z1"]= str(Result.loc[0, "L1_SiltTotal"])
        jsonupdate_sol[solmk]["line9_silt"]["z2"]= str(Result.loc[0, "L2_SiltTotal"])
        jsonupdate_sol[solmk]["line9_silt"]["z3"]= str(Result.loc[0, "L3_SiltTotal"])
        jsonupdate_sol[solmk]["line9_silt"]["z4"]= str(Result.loc[0, "L4_SiltTotal"])
        jsonupdate_sol[solmk]["line9_silt"]["z5"]= str(Result.loc[0, "L5_SiltTotal"])
        jsonupdate_sol[solmk]["line9_silt"]["z6"]= str(Result.loc[0, "L6_SiltTotal"])
        jsonupdate_sol[solmk]["line9_silt"]["z7"]= str(Result.loc[0, "L7_SiltTotal"])
        jsonupdate_sol[solmk]["line9_silt"]["z8"]= str(Result.loc[0, "L8_SiltTotal"])
        jsonupdate_sol[solmk]["line9_silt"]["z9"]= str(Result.loc[0, "L9_SiltTotal"])
        jsonupdate_sol[solmk]["line9_silt"]["z10"]= str(Result.loc[0, "L10_SiltTotal"])


        jsonupdate_sol[solmk]["line11_ph"]["z1"]= str(Result.loc[0, "L1_PH"])
        jsonupdate_sol[solmk]["line11_ph"]["z2"]= str(Result.loc[0, "L2_PH"])
        jsonupdate_sol[solmk]["line11_ph"]["z3"]= str(Result.loc[0, "L3_PH"])
        jsonupdate_sol[solmk]["line11_ph"]["z4"]= str(Result.loc[0, "L4_PH"])
        jsonupdate_sol[solmk]["line11_ph"]["z5"]= str(Result.loc[0, "L5_PH"])
        jsonupdate_sol[solmk]["line11_ph"]["z6"]= str(Result.loc[0, "L6_PH"])
        jsonupdate_sol[solmk]["line11_ph"]["z7"]= str(Result.loc[0, "L7_PH"])
        jsonupdate_sol[solmk]["line11_ph"]["z8"]= str(Result.loc[0, "L8_PH"])
        jsonupdate_sol[solmk]["line11_ph"]["z9"]= str(Result.loc[0, "L9_PH"])
        jsonupdate_sol[solmk]["line11_ph"]["z10"]= str(Result.loc[0, "L10_PH"])

        jsonupdate_sol[solmk]["line12_sumofbase_smb"]["z1"]= str(Result.loc[0, "L1_SumofBases"])
        jsonupdate_sol[solmk]["line12_sumofbase_smb"]["z2"]= str(Result.loc[0, "L2_SumofBases"])
        jsonupdate_sol[solmk]["line12_sumofbase_smb"]["z3"]= str(Result.loc[0, "L3_SumofBases"])
        jsonupdate_sol[solmk]["line12_sumofbase_smb"]["z4"]= str(Result.loc[0, "L4_SumofBases"])
        jsonupdate_sol[solmk]["line12_sumofbase_smb"]["z5"]= str(Result.loc[0, "L5_SumofBases"])
        jsonupdate_sol[solmk]["line12_sumofbase_smb"]["z6"]= str(Result.loc[0, "L6_SumofBases"])
        jsonupdate_sol[solmk]["line12_sumofbase_smb"]["z7"]= str(Result.loc[0, "L7_SumofBases"])
        jsonupdate_sol[solmk]["line12_sumofbase_smb"]["z8"]= str(Result.loc[0, "L8_SumofBases"])
        jsonupdate_sol[solmk]["line12_sumofbase_smb"]["z9"]= str(Result.loc[0, "L9_SumofBases"])
        jsonupdate_sol[solmk]["line12_sumofbase_smb"]["z10"]= str(Result.loc[0, "L10_SumofBases"])

        jsonupdate_sol[solmk]["line13_orgc_conc_woc"]["z1"]= str(Result.loc[0, "L1_OrganicMatter"])
        jsonupdate_sol[solmk]["line13_orgc_conc_woc"]["z2"]= str(Result.loc[0, "L2_OrganicMatter"])
        jsonupdate_sol[solmk]["line13_orgc_conc_woc"]["z3"]= str(Result.loc[0, "L3_OrganicMatter"])
        jsonupdate_sol[solmk]["line13_orgc_conc_woc"]["z4"]= str(Result.loc[0, "L4_OrganicMatter"])
        jsonupdate_sol[solmk]["line13_orgc_conc_woc"]["z5"]= str(Result.loc[0, "L5_OrganicMatter"])
        jsonupdate_sol[solmk]["line13_orgc_conc_woc"]["z6"]= str(Result.loc[0, "L6_OrganicMatter"])
        jsonupdate_sol[solmk]["line13_orgc_conc_woc"]["z7"]= str(Result.loc[0, "L7_OrganicMatter"])
        jsonupdate_sol[solmk]["line13_orgc_conc_woc"]["z8"]= str(Result.loc[0, "L8_OrganicMatter"])
        jsonupdate_sol[solmk]["line13_orgc_conc_woc"]["z9"]= str(Result.loc[0, "L9_OrganicMatter"])
        jsonupdate_sol[solmk]["line13_orgc_conc_woc"]["z10"]= str(Result.loc[0, "L10_OrganicMatter"])

        jsonupdate_sol[solmk]["line14_caco3_cac"]["z1"]= str(Result.loc[0, "L1_CaCO3"])
        jsonupdate_sol[solmk]["line14_caco3_cac"]["z2"]= str(Result.loc[0, "L2_CaCO3"])
        jsonupdate_sol[solmk]["line14_caco3_cac"]["z3"]= str(Result.loc[0, "L3_CaCO3"])
        jsonupdate_sol[solmk]["line14_caco3_cac"]["z4"]= str(Result.loc[0, "L4_CaCO3"])
        jsonupdate_sol[solmk]["line14_caco3_cac"]["z5"]= str(Result.loc[0, "L5_CaCO3"])
        jsonupdate_sol[solmk]["line14_caco3_cac"]["z6"]= str(Result.loc[0, "L6_CaCO3"])
        jsonupdate_sol[solmk]["line14_caco3_cac"]["z7"]= str(Result.loc[0, "L7_CaCO3"])
        jsonupdate_sol[solmk]["line14_caco3_cac"]["z8"]= str(Result.loc[0, "L8_CaCO3"])
        jsonupdate_sol[solmk]["line14_caco3_cac"]["z9"]= str(Result.loc[0, "L9_CaCO3"])
        jsonupdate_sol[solmk]["line14_caco3_cac"]["z10"]= str(Result.loc[0, "L10_CaCO3"])

        jsonupdate_sol[solmk]["line15_cec"]["z1"]= str(Result.loc[0, "L1_CEC"])
        jsonupdate_sol[solmk]["line15_cec"]["z2"]= str(Result.loc[0, "L2_CEC"])
        jsonupdate_sol[solmk]["line15_cec"]["z3"]= str(Result.loc[0, "L3_CEC"])
        jsonupdate_sol[solmk]["line15_cec"]["z4"]= str(Result.loc[0, "L4_CEC"])
        jsonupdate_sol[solmk]["line15_cec"]["z5"]= str(Result.loc[0, "L5_CEC"])
        jsonupdate_sol[solmk]["line15_cec"]["z6"]= str(Result.loc[0, "L6_CEC"])
        jsonupdate_sol[solmk]["line15_cec"]["z7"]= str(Result.loc[0, "L7_CEC"])
        jsonupdate_sol[solmk]["line15_cec"]["z8"]= str(Result.loc[0, "L8_CEC"])
        jsonupdate_sol[solmk]["line15_cec"]["z9"]= str(Result.loc[0, "L9_CEC"])
        jsonupdate_sol[solmk]["line15_cec"]["z10"]= str(Result.loc[0, "L10_CEC"])

        jsonupdate_sol[solmk]["line16_rock_rok"]["z1"]= str(Result.loc[0, "L1_CroaseFragment"])
        jsonupdate_sol[solmk]["line16_rock_rok"]["z2"]= str(Result.loc[0, "L2_CroaseFragment"])
        jsonupdate_sol[solmk]["line16_rock_rok"]["z3"]= str(Result.loc[0, "L3_CroaseFragment"])
        jsonupdate_sol[solmk]["line16_rock_rok"]["z4"]= str(Result.loc[0, "L4_CroaseFragment"])
        jsonupdate_sol[solmk]["line16_rock_rok"]["z5"]= str(Result.loc[0, "L5_CroaseFragment"])
        jsonupdate_sol[solmk]["line16_rock_rok"]["z6"]= str(Result.loc[0, "L6_CroaseFragment"])
        jsonupdate_sol[solmk]["line16_rock_rok"]["z7"]= str(Result.loc[0, "L7_CroaseFragment"])
        jsonupdate_sol[solmk]["line16_rock_rok"]["z8"]= str(Result.loc[0, "L8_CroaseFragment"])
        jsonupdate_sol[solmk]["line16_rock_rok"]["z9"]= str(Result.loc[0, "L9_CroaseFragment"])
        jsonupdate_sol[solmk]["line16_rock_rok"]["z10"]= str(Result.loc[0, "L10_CroaseFragment"])

        jsonupdate_sol[solmk]["line17_inisolnconc_cnds"]["z1"]= "0.00"
        jsonupdate_sol[solmk]["line17_inisolnconc_cnds"]["z2"]= "0.00"
        jsonupdate_sol[solmk]["line17_inisolnconc_cnds"]["z3"]= "0.00"
        jsonupdate_sol[solmk]["line17_inisolnconc_cnds"]["z4"]= "0.00"
        jsonupdate_sol[solmk]["line17_inisolnconc_cnds"]["z5"]= "0.00"
        jsonupdate_sol[solmk]["line17_inisolnconc_cnds"]["z6"]= "0.00"
        jsonupdate_sol[solmk]["line17_inisolnconc_cnds"]["z7"]= "0.00"
        jsonupdate_sol[solmk]["line17_inisolnconc_cnds"]["z8"]= "0.00"
        jsonupdate_sol[solmk]["line17_inisolnconc_cnds"]["z9"]= "0.00"
        jsonupdate_sol[solmk]["line17_inisolnconc_cnds"]["z10"]= "0.00"

        jsonupdate_sol[solmk]["line18_soilp_ssf"]["z1"]= str(Result.loc[0, "L1_ph2osoluble_r"])
        jsonupdate_sol[solmk]["line18_soilp_ssf"]["z2"]= str(Result.loc[0, "L2_ph2osoluble_r"])
        jsonupdate_sol[solmk]["line18_soilp_ssf"]["z3"]= str(Result.loc[0, "L3_ph2osoluble_r"])
        jsonupdate_sol[solmk]["line18_soilp_ssf"]["z4"]= str(Result.loc[0, "L4_ph2osoluble_r"])
        jsonupdate_sol[solmk]["line18_soilp_ssf"]["z5"]= str(Result.loc[0, "L5_ph2osoluble_r"])
        jsonupdate_sol[solmk]["line18_soilp_ssf"]["z6"]= str(Result.loc[0, "L6_ph2osoluble_r"])
        jsonupdate_sol[solmk]["line18_soilp_ssf"]["z7"]= str(Result.loc[0, "L7_ph2osoluble_r"])
        jsonupdate_sol[solmk]["line18_soilp_ssf"]["z8"]= str(Result.loc[0, "L8_ph2osoluble_r"])
        jsonupdate_sol[solmk]["line18_soilp_ssf"]["z9"]= str(Result.loc[0, "L9_ph2osoluble_r"])
        jsonupdate_sol[solmk]["line18_soilp_ssf"]["z10"]= str(Result.loc[0, "L10_ph2osoluble_r"])

        jsonupdate_sol[solmk]["line20_drybd_bdd"]["z1"]= "0.00"
        jsonupdate_sol[solmk]["line20_drybd_bdd"]["z2"]= "0.00"
        jsonupdate_sol[solmk]["line20_drybd_bdd"]["z3"]= "0.00"
        jsonupdate_sol[solmk]["line20_drybd_bdd"]["z4"]= "0.00"
        jsonupdate_sol[solmk]["line20_drybd_bdd"]["z5"]= "0.00"
        jsonupdate_sol[solmk]["line20_drybd_bdd"]["z6"]= "0.00"
        jsonupdate_sol[solmk]["line20_drybd_bdd"]["z7"]= "0.00"
        jsonupdate_sol[solmk]["line20_drybd_bdd"]["z8"]= "0.00"
        jsonupdate_sol[solmk]["line20_drybd_bdd"]["z9"]= "0.00"
        jsonupdate_sol[solmk]["line20_drybd_bdd"]["z10"]= "0.00"

        jsonupdate_sol[solmk]["line22_ksat"]["z1"]= str(Result.loc[0, "L1_KSat"])
        jsonupdate_sol[solmk]["line22_ksat"]["z2"]= str(Result.loc[0, "L2_KSat"])
        jsonupdate_sol[solmk]["line22_ksat"]["z3"]= str(Result.loc[0, "L3_KSat"])
        jsonupdate_sol[solmk]["line22_ksat"]["z4"]= str(Result.loc[0, "L4_KSat"])
        jsonupdate_sol[solmk]["line22_ksat"]["z5"]= str(Result.loc[0, "L5_KSat"])
        jsonupdate_sol[solmk]["line22_ksat"]["z6"]= str(Result.loc[0, "L6_KSat"])
        jsonupdate_sol[solmk]["line22_ksat"]["z7"]= str(Result.loc[0, "L7_KSat"])
        jsonupdate_sol[solmk]["line22_ksat"]["z8"]= str(Result.loc[0, "L8_KSat"])
        jsonupdate_sol[solmk]["line22_ksat"]["z9"]= str(Result.loc[0, "L9_KSat"])
        jsonupdate_sol[solmk]["line22_ksat"]["z10"]= str(Result.loc[0, "L10_KSat"])

        jsonupdate_sol[solmk]["line24_orgp_wpo"]["z1"]= "0.00"
        jsonupdate_sol[solmk]["line24_orgp_wpo"]["z2"]= "0.00"
        jsonupdate_sol[solmk]["line24_orgp_wpo"]["z3"]= "0.00"
        jsonupdate_sol[solmk]["line24_orgp_wpo"]["z4"]= "0.00"
        jsonupdate_sol[solmk]["line24_orgp_wpo"]["z5"]= "0.00"
        jsonupdate_sol[solmk]["line24_orgp_wpo"]["z6"]= "0.00"
        jsonupdate_sol[solmk]["line24_orgp_wpo"]["z7"]= "0.00"
        jsonupdate_sol[solmk]["line24_orgp_wpo"]["z8"]= "0.00"
        jsonupdate_sol[solmk]["line24_orgp_wpo"]["z9"]= "0.00"
        jsonupdate_sol[solmk]["line24_orgp_wpo"]["z10"]= "0.00"

        jsonupdate_sol[solmk]["line26_electricalcond_ec"]["z1"]= str(Result.loc[0, "L1_EC"])
        jsonupdate_sol[solmk]["line26_electricalcond_ec"]["z2"]= str(Result.loc[0, "L2_EC"])
        jsonupdate_sol[solmk]["line26_electricalcond_ec"]["z3"]= str(Result.loc[0, "L3_EC"])
        jsonupdate_sol[solmk]["line26_electricalcond_ec"]["z4"]= str(Result.loc[0, "L4_EC"])
        jsonupdate_sol[solmk]["line26_electricalcond_ec"]["z5"]= str(Result.loc[0, "L5_EC"])
        jsonupdate_sol[solmk]["line26_electricalcond_ec"]["z6"]= str(Result.loc[0, "L6_EC"])
        jsonupdate_sol[solmk]["line26_electricalcond_ec"]["z7"]= str(Result.loc[0, "L7_EC"])
        jsonupdate_sol[solmk]["line26_electricalcond_ec"]["z8"]= str(Result.loc[0, "L8_EC"])
        jsonupdate_sol[solmk]["line26_electricalcond_ec"]["z9"]= str(Result.loc[0, "L9_EC"])
        jsonupdate_sol[solmk]["line26_electricalcond_ec"]["z10"]= str(Result.loc[0, "L10_EC"])

        jsonupdate_sol[solmk]["layerid"]["z1"]= str(Result.loc[0, "L1_layerid"])
        jsonupdate_sol[solmk]["layerid"]["z2"]= str(Result.loc[0, "L2_layerid"])
        jsonupdate_sol[solmk]["layerid"]["z3"]= str(Result.loc[0, "L3_layerid"])
        jsonupdate_sol[solmk]["layerid"]["z4"]= str(Result.loc[0, "L4_layerid"])
        jsonupdate_sol[solmk]["layerid"]["z5"]= str(Result.loc[0, "L5_layerid"])
        jsonupdate_sol[solmk]["layerid"]["z6"]= str(Result.loc[0, "L6_layerid"])
        jsonupdate_sol[solmk]["layerid"]["z7"]= str(Result.loc[0, "L7_layerid"])
        jsonupdate_sol[solmk]["layerid"]["z8"]= str(Result.loc[0, "L8_layerid"])
        jsonupdate_sol[solmk]["layerid"]["z9"]= str(Result.loc[0, "L9_layerid"])
        jsonupdate_sol[solmk]["layerid"]["z10"]= str(Result.loc[0, "L10_layerid"])
        
        return jsonupdate_sol




    @staticmethod
    def writerunsoljson(fin_soillujson: str,
                    fin_soiltempjson: str, 
                    fout_runsoltempjson: str):
        
        # Read in two json files
        # Read in the soillu for watershed json
        with open(fin_soillujson) as json_file:
            sollujson = json.loads(json_file.read())
        json_file.close()
        # Read in the template soil json
        with open(fin_soiltempjson) as json_file:
            tmpjson = json.loads(json_file.read())
        json_file.close()        

        # Get unique soil id values
        sollst = []

        for k, v in sollujson.items():
            sollst.append(v['mukey'])

        sollst = list(set(sollst))

        # Get soil json template, create a template
        # for each soil needed.
        for sidx in sollst:
            tmpjson[sidx] = tmpjson['soil1']

        del tmpjson['soil1']

        with open(fout_runsoltempjson, 'w') as outfile:
            json.dump(tmpjson, outfile)

        return tmpjson




    @staticmethod
    def writeSolCOM(fnapexrunsce: str,
                    fnsollujson: str,
                    fnsolcom: str):

        # Readin the JSON contents from 
        with open(fnsollujson) as json_file:
            sollulatlong = json.loads(json_file.read())

        json_file.close()

        # Remove the file if it exist
        if os.path.isfile(fnsolcom):
            os.remove(fnsolcom)

        # Open file, write contents and then close the file
        outfid_solcom = 0
        outfid_solcom = open(fnsolcom, "w")

        for key, value in sollulatlong.items():
            outfid_solcom.writelines("%5s\tSOL%s.SOL\n" %(key,
                                              value['mukey']))

        outfid_solcom.close()



    @staticmethod
    def convtif2shp(fntif: str, fnshp: str):
        """Use appropriate path separator."""
        
        procCommand = """gdal_polygonize.py -of "ESRI Shapefile"  %s %s""" %(
                fntif, fnshp
                ) 
        generalfuncs.addToLog(procCommand)
        # os.system(procCommand)
        #o=os.popen(procCommand).read()
        
        ## call date command ##
        p = subprocess.Popen(procCommand, stdout=subprocess.PIPE, shell=True)
        


    #######################################################



    #######################################################
    def writesolcomline(self, fidsolcom, sollulatlong):

        for key, value in sollulatlong.items():
            fidsolcom.writelines("%5s\tSOL%s.SOL\n" %(key,
                                              value['mukey']))




    #######################################################
    def closecomfiles(self, fid):

        fid.close()


#