# -*- coding: utf-8 -*-
#***************************************************************************/
import os, sys
from time import gmtime, strftime
import importlib,  pip


class globalsetting:
    """Data used across across the plugin, and some utilities on it."""
    def __init__(self):
      
#        self.logfilename = "log%s.txt" %(strftime("%Y_%m_%d", gmtime()))
        self.logfilename = "log.txt"
        
        self.gdalscripts = r"C:\Program Files\QGIS 3.4\apps\Python37\Scripts"
        
        self.osplatform = self.get_osplatform()
        
        # Setup taudem and apex paths
        # input output scenarios
        # APEX Database 
        self.fdScripts = "scripts"

        self.fnGdalReclassPy = os.path.join(self.fdScripts, "gdal_reclassify.py")
        self.fdTauDEM = os.path.join(self.fdScripts, "taudembins")

        self.fdclinearbin =  os.path.join(self.fdScripts, "clinear")
        if self.osplatform == "linux":
            self.fnapexbin = "apex15011911"
            self.fdtaudembin = os.path.join(self.fdTauDEM, 
                                        "taudembin53964")
            self.fnclisearch =  os.path.join(self.fdclinearbin, 
                                        "climNearest")
            self.mpiexecPath = 'mpiexec'
                                        
        elif self.osplatform == "Windows":
            self.fnapexbin = "apex1501191119Rel64.exe"
            self.fdtaudembin = os.path.join(self.fdTauDEM, 
                                        "taudemexe53964")
            self.fnclisearch =  os.path.join(self.fdclinearbin, 
                                        "climnearstn.exe")
                    
            self.mpiexecPath = r'C:\\Program Files\\Microsoft MPI\Bin\\mpiexec.exe'
            
                      



    def get_osplatform(self):

        platforms = {
            'linux1' : 'Linux',
            'linux2' : 'Linux',
            'darwin' : 'OS X',
            'win32' : 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform

        return platforms[sys.platform]