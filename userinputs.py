# -*- coding: utf-8 -*-
#***************************************************************************/
import os
#***************************************************************************/

class userinputs():
    """Data used across across the plugin, and some utilities on it."""
    def __init__(self):
        
        # User have to select the right mode to run the corresponding
        # script.
        # This program provides the following modes of setting up apex:
        # 1. watershed-mode: mode 1
        # 2. boundaryws-mode: mode 2
        self.runMode = "mode1"
        self.fnprojName = "demo"
     
        # input output scenarios
        self.fdMain = os.getcwd()
        
        self.fdApexProjMain = os.path.join(self.fdMain, "apexprojects_demo")

        self.fnApexProj = "{}{}".format(self.fnprojName, self.runMode)

        # The boundary could be a shapefile or tif file
        # They need to have a UTM projection for corresponding zones.
        self.fnUserBdy = "boundary.shp"

        # The outlet need to be a point shapefile.
        self.fnOutlet = "outlet.shp"
        
        # MPI Settings:
        # If user would like to use multiprocesses to run Taudem, specify 
        # the value to desired processers.
        # numProcessers:
        # number of processes used for simulation
        # 0: for only using 1 processer
        # n: for using n no of processers
        self.numProcessers = 11
        
        # Watershed delineation settings:
        self.channelThreshold = "10000"
        

        # TODO: Add the functions for adding burnin files.
        self.burnfile = ""
        self.useburnin = False
        
        # Specify whether daily data will be used.
        self.useDlyWea = False
        self.dailyWeaVar = ["prcp", "tmax", "tmin"]

        # Specify whether user would like to use their own soil database
        self.useUserSoil = False

        # Spedify whether user would like tu prepare their own ops files
        self.userUserLUOPS = False

        # Specify slope groups
        # The watershed might have a lot of slope numbers. 
        # These slopes were grouped to user specified groups.
        self.usrSlpGroupBins = [0, 2, 5, 9999]

        # Snapping distance of outlet to stream cells
        self.mvOltSnapDist = "300"


        self.fdApexProj = os.path.join(self.fdApexProjMain,
                        self.fnApexProj)

        self.fdUserDly = os.path.join(self.fdApexProj, 
                                "userdlyandlist")
        self.fnUserDlyListdb = os.path.join(self.fdUserDly, 
                                "exampleDlyList.db")

        self.dbUsrSoil = os.path.join(self.fdApexProj,
                "usersoil.db")
        self.tbUsrSoil = "usersoil"

        self.fdGIS = os.path.join(self.fdApexProj,
                        "gislayers")
        
        self.fnDem = os.path.join(self.fdGIS,
                                    "demUTM.tif"
                                    )

        self.fnLandUse = os.path.join(self.fdGIS,
                                    "landuseUTM.tif"
                                    )   

        self.fnSoil = os.path.join(self.fdGIS,
                                    "soilUTM.tif"
                                    ) 

        self.fnpOutLet = os.path.join(self.fdGIS,
                                    self.fnOutlet
                                    )    
        self.fnpUsrBdy = os.path.join(self.fdGIS,
                                    self.fnUserBdy
                                    )
    
        self.fdUsrLuOpsFiles = os.path.join(
            self.fdApexProj, "userlulistopcfiles"
        )

        self.fnUsrTbLulists = os.path.join(
            self.fdUsrLuOpsFiles, "user_lumgtupn.csv"
        )
        # Not used now
        self.streamThreshold = "20000"
            