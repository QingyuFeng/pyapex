# -*- coding: utf-8 -*-
#***************************************************************************/
import os
#***************************************************************************/

class defaultFNFD():
    """Data used across across the plugin, and some utilities on it."""
    def __init__(self, userinputs):
        
        self.fdTauLayers = os.path.join(userinputs.fdApexProj,
                        "taudemlayers")
        
        (self.baseOlt, self.suffixOlt) = os.path.splitext(userinputs.fnOutlet)
        self.fnpMvOlt = os.path.join(self.fdTauLayers,
                                    'mvOlt' + self.suffixOlt)

        self.usrslpgroup = userinputs.usrSlpGroupBins
        
        self.fdApexTio = os.path.join(userinputs.fdApexProj,
                                "apextio")

        self.fdUsrdlylst = os.path.join(userinputs.fdApexProj,
                                "userdlyandlist")

        # APEX Database 
        self.fdScripts = "scripts"
                                    
        self.fdApexData = os.path.join(self.fdScripts,
                                 "apexdata")

        # Database name: default
        self.dbfnCliSol = os.path.join(self.fdApexData,
                                    'apexSoilCligenChinaData.sqlite')
        self.tbDftSoil = 'soter2apex'
        self.tbwgncfsr = "wgncfsr"

        self.fdJSON = os.path.join(self.fdScripts, "json")

        (self.base, self.suffix) = os.path.splitext(userinputs.fnDem)
        self.baseName = os.path.split(self.base)[1]
        self.fnFel = self.baseName + 'fel' + self.suffix
        self.fnpFel = os.path.join(self.fdTauLayers,
                                   self.fnFel)

        self.fnSd8 = 'sd8Slp' + self.suffix
        self.fnP = 'pFlowDir' + self.suffix
        self.fnpSd8 = os.path.join(self.fdTauLayers,
                                   self.fnSd8)
        self.fnpP = os.path.join(self.fdTauLayers,
                                   self.fnP)

        self.fnSlp = 'dInfSlp' + self.suffix
        self.fnAng = self.baseName + 'dInfAng' + self.suffix
        self.fnpSlp = os.path.join(self.fdTauLayers,
                                   self.fnSlp)
        self.fnpAng = os.path.join(self.fdTauLayers,
                                   self.fnAng) 
                    
        self.fnAd8 = 'ad8ContriArea' + self.suffix
        self.fnpAd8 = os.path.join(self.fdTauLayers,
                                   self.fnAd8)

        self.fnSca = 'sca' + self.suffix
        self.fnpSca = os.path.join(self.fdTauLayers,
                                   self.fnSca)

        self.fnGord = 'gord' + self.suffix
        self.fnPlen = 'plen' + self.suffix
        self.fnTlen = 'tlen' + self.suffix
        self.fnpGord = os.path.join(self.fdTauLayers,
                                           self.fnGord)
        self.fnpPlen = os.path.join(self.fdTauLayers,
                                           self.fnPlen)
        self.fnpTlen = os.path.join(self.fdTauLayers,
                                           self.fnTlen) 

        self.fnSrcStream = 'srcStrNet' + self.suffix
        self.fnpSrcStream = os.path.join(self.fdTauLayers,
                                           self.fnSrcStream) 

        self.fnOrd = 'ord' + self.suffix
        self.fnStreamShp = 'stream.shp'
        self.fnTree = 'tree.txt'
        self.fnCoord = 'coord.txt'
        self.fnSubWsFull = 'wsbdy' + self.suffix
        
        self.fnpOrd = os.path.join(self.fdTauLayers,
                                           self.fnOrd) 
        self.fnpStreamShp = os.path.join(self.fdTauLayers,
                                           self.fnStreamShp)
        self.fnpTree = os.path.join(self.fdTauLayers,
                                           self.fnTree)
        self.fnpCoord = os.path.join(self.fdTauLayers,
                                           self.fnCoord)
        self.fnpSubWsFull = os.path.join(self.fdTauLayers,
                                           self.fnSubWsFull)

        self.fnpSubWsShp = os.path.join(self.fdTauLayers, 'wsbdyshp.shp')

        self.fnSrcStreamAsc = self.baseName + 'srcStream.asc'
        self.fnpSrcStreamAsc = os.path.join(self.fdTauLayers,
                                           self.fnSrcStreamAsc) 

        # Input Output for function: clipRasterbyShp to user boundary
        self.fnsubWsUsrBdy = "subWsUsrBdy" + self.suffix
        self.fnpSubWsUsrBdy = os.path.join(self.fdTauLayers,
                                           self.fnsubWsUsrBdy) 
        
        self.fnSubWsUsrBdyAsc = "subWsUsrBdy.asc"
        self.fnpSubWsUsrBdyAsc = os.path.join(self.fdTauLayers,
                                           self.fnSubWsUsrBdyAsc) 
        self.fnSubWsAsc = "subWs.asc"
        self.fnpSubWsAsc = os.path.join(self.fdTauLayers,
                                           self.fnSubWsAsc) 

        self.fdRecWSTif = os.path.join(self.fdTauLayers,
                                        "reclassifiedWs") 
        
        self.fnpSubRecPair = os.path.join(self.fdRecWSTif, 
            "demwreclasspair.json")


        # Input output for extracting landuse to watershed extent
        (self.baselu, self.suffixlu) = os.path.splitext(userinputs.fnLandUse)
        self.baseLuName = os.path.split(self.baselu)[1]

        self.fnwsExtLu = 'luwsext' + self.suffix
        self.fnpWsExtLu = os.path.join(self.fdTauLayers,
                                           self.fnwsExtLu)

        self.fnUsrBdyLu = 'luUsrBdy' + self.suffix
        self.fnpUsrBdyLu = os.path.join(self.fdTauLayers,
                                           self.fnUsrBdyLu)
        self.fnUsrBdyLuAsc = 'luUsrBdy.asc'
        self.fnpUsrBdyLuAsc = os.path.join(self.fdTauLayers,
                                           self.fnUsrBdyLuAsc)
        self.fnUsrBdyDEM = 'demUsrBdy' + self.suffix
        self.fnpUsrBdyDEM = os.path.join(self.fdTauLayers,
                                           self.fnUsrBdyDEM)
        self.fnUsrBdyDEMAsc = 'demUsrBdy.asc'
        self.fnpUsrBdyDEMAsc = os.path.join(self.fdTauLayers,
                                           self.fnUsrBdyDEMAsc)                                           


        # Input output for extracting soil to watershed extent
        (self.basesol, self.suffixsol) = os.path.splitext(userinputs.fnSoil)
        self.basesolName = os.path.split(self.basesol)[1]

        self.fnWsExtSoil = 'solwsext' + self.suffix
        self.fnpWsExtSoil = os.path.join(self.fdTauLayers,
                                           self.fnWsExtSoil)
        self.fnUsrBdySol = 'solUsrBdy' + self.suffix
        self.fnpUsrBdySol = os.path.join(self.fdTauLayers,
                                           self.fnUsrBdySol)
        self.fnUsrBdySolAsc = 'solUsrBdy.asc'
        self.fnpUsrBdySolAsc = os.path.join(self.fdTauLayers,
                                           self.fnUsrBdySolAsc)

        # Input output for function: procTifs2Ascs
        self.fnPlenAsc = 'plen.asc'
        self.fnpPlenAsc = os.path.join(self.fdApexTio,
                                           self.fnPlenAsc)

        self.fnDemAsc = 'demfel.asc'
        self.fnpDemASC = os.path.join(self.fdApexTio,
                                           self.fnDemAsc)

        self.fnWsExtLuAsc = 'lu.asc'
        self.fnpWsExtLuAsc = os.path.join(self.fdApexTio,
                                           self.fnWsExtLuAsc)

        self.fnWsExtSolAsc = 'sol.asc'
        self.fnpWsExtSolAsc = os.path.join(self.fdApexTio,
                                           self.fnWsExtSolAsc)

        self.fnSd8Asc = 'slp.asc'
        self.fnpSd8Asc = os.path.join(self.fdApexTio,
                                   self.fnSd8Asc)

        self.fnWsStreamAsc = 'strm.asc'
        self.fnpWsStreamAsc = os.path.join(self.fdApexTio,
                                           self.fnWsStreamAsc)

        # Input output for function: preAPEXJSONOlt
        self.jsonVarSubWsTemp = os.path.join(self.fdJSON,
                    "var1wssub.json")
        self.jsonVarSubWsSce = os.path.join(self.fdApexTio,
                    "var1wssub.json")
        self.jsonSitTemp = os.path.join(self.fdJSON,
                    "tmpsitefile.json")
        self.jsonSitSce = os.path.join(self.fdApexTio,
                    "tmpsitefile.json")
        self.jsonSubSce = os.path.join(self.fdApexTio,
                    "runsub.json")
        self.jsonSubWsSolLuLL = os.path.join(self.fdApexTio,
                    "wssubsollulatlon.json")
        self.jsonSitSceRun = os.path.join(self.fdApexTio,
                    "runsite.json")

        self.fnpJSONWSRunNames = os.path.join(self.fdApexTio,
                    "runwsnames.json")


        # APEX data 
        if userinputs.userUserLUOPS:
            self.tblumgtupn = userinputs.fnUsrTbLulists
        else:
            self.tblumgtupn = os.path.join(self.fdApexData,
                            "table_lumgtupn.csv")
        self.tbchn = os.path.join(self.fdApexData,
                            "table_chn.txt")

        # Input output for function: writeSOL
        self.jsonSolTemp = os.path.join(self.fdJSON,
                    "tmpsolfile.json")
        self.jsonSolSce = os.path.join(self.fdApexTio,
                    "tmpsolfile.json")
        self.jsonSolSceRun = os.path.join(self.fdApexTio,
                    "runsol.json")

        self.fnpSolCom = os.path.join(self.fdApexTio,
                            "SOILCOM.DAT")
        
        self.fdDLYFiles = "dlyWithListFiles"
        self.fnpMonStnListdb = os.path.join(
                        self.fdScripts,
                        "clinear",
                        "cfsrchinastn.db"
                        )                
        self.fnFoundStn = os.path.join(
                        self.fdApexTio,
                        "station.txt"
                        )   

        # APEX Climate COM files: dly, wp1, wnd
        self.fnapexdlycomTemp = os.path.join(
                        self.fdApexData,
                        "WDLSTCOM.DAT"
                        ) 
        self.fnapexdlycom = os.path.join(
                        self.fdApexTio,
                        "WDLSTCOM.DAT"
                        ) 
        self.fnapexwp1com = os.path.join(
                        self.fdApexTio,
                        "WPM1COM.DAT"
                        )  
        self.fnapexwndcom = os.path.join(
                        self.fdApexTio,
                        "WINDCOM.DAT"
                        )   

        # Write SITCOM and related file
        self.fnpSITCOM = os.path.join(
                        self.fdApexTio,
                        "SITECOM.DAT"
                        ) 
        self.fnpSIT = os.path.join(
                        self.fdApexTio,
                        "SIT1.SIT"
                        ) 
            
        # Copy OPS files
        if userinputs.userUserLUOPS:
            self.fdopssrc = userinputs.fdUsrLuOpsFiles
        else:
            self.fdopssrc = os.path.join(self.fdApexData,
                            "OPSCDFT"
                            )

        # Write SITCOM and related file
        self.fnSubAllCOM = os.path.join(
                        self.fdApexTio,
                        "SUBACOM.DAT"
                        ) 

        # Write the control file
        self.jsonContTemp = os.path.join(
                        self.fdJSON,
                        "tmpcontfile.json")
        self.jsonContRun = os.path.join(
                        self.fdApexTio,
                        "runcont.json")
        self.fnpCont = os.path.join(
                        self.fdApexTio,
                        "APEXCONT.DAT")
        
        # Write OPSCCOM file
        self.fnpOPSCOM = os.path.join(
                        self.fdApexTio,
                        "OPSCCOM.DAT")

        # Write APEXRUN file
        self.fnpAPEXRUN = os.path.join(
                        self.fdApexTio,
                        "APEXRUN.DAT")


        # For mapping
        self.fnpJSONQSNPLvls = os.path.join(
            self.fdJSON, "qsnplevels.json")
        
        self.fnpSubWQQSNPLvls = os.path.join(
            self.fdApexTio, 
            "subQSNPValLvl.json")