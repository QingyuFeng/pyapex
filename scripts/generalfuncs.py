# -*- coding: utf-8 -*-

# Import python standard libraries
import os
import json
import posixpath
import ntpath
from time import gmtime, strftime
import pathlib

class generalfuncs:
    """Various utilities."""
        
    @staticmethod
    def join(path: str, fileName: str) -> str:
        """Use appropriate path separator."""
        if os.name == 'nt':
            return ntpath.join(path, fileName)
        else:
            return posixpath.join(path, fileName)

    @staticmethod
    def isUpToDate(inFile: str, outFile: str) -> bool:
        """Return true (outFile is up to date) if inFile exists, outFile exists and is no younger than inFile."""
        if not os.path.exists(inFile):
            return False
        if os.path.exists(outFile):
            if os.path.getmtime(outFile) >= os.path.getmtime(inFile):
                return True
        return False



    @staticmethod
    def removeFileifExist(file2bremove) -> None:
        """remove file if exists """
        
        if os.path.exists(file2bremove):
            os.remove(file2bremove)
        
        

    @staticmethod
    def checkExists(fileName):
        """
        Check whether file exists
        """
        if fileName == '' or not pathlib.Path(fileName).exists():
            print('Error: {} is not found !!!'.format(fileName))
            exit()



    @staticmethod
    def addToLog(messages: str) -> None:
        
#        print(globalsetting.logfilename())
#        logfn = globalsetting.logfilename()
        fid = open("log.txt", "a")
        lfw = "%s | %s\n" %(strftime("%Y_%m_%d  %H:%M:%S", gmtime()), messages)
        fid.writelines(lfw)
        fid.close()

    @staticmethod
    def readJSON(fnJson):
        inf_usrjson = {}
        with open(fnJson) as json_file:    
            inf_usrjson = json.loads(json_file.read())

        return inf_usrjson

    @staticmethod
    def writeJSONToFile(fnJson, jsonCont):
        with open(fnJson, 'w') as outfile:
            json.dump(jsonCont, outfile)





    