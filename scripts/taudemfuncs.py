# -*- coding: utf-8 -*-
# Import python standard libraries
import os
import subprocess
import pathlib

# Import pyapex functions
from .generalfuncs import generalfuncs
from .globalsetting import globalsetting

generalfuncs = generalfuncs()
globalsetting = globalsetting()


class taudemfuncs:
    """Various utilities."""

    @staticmethod
    def runPitFill(demFile, felFile, numProcesses):
        """Run PitFill."""

        if globalsetting.osplatform == "linux":
            fntool = 'pitremove'
        elif globalsetting.osplatform == "Windows":
            fntool = 'PitRemove.exe'

        return taudemfuncs.run(fntool,
                               [('-z', demFile)],
                               [],
                               [('-fel', felFile)], 
                               numProcesses, 
                               False)
        

    @staticmethod
    def runD8FlowDir(felFile, sd8File, pFile, numProcesses):
        """Run D8FlowDir."""
        
        if globalsetting.osplatform == "linux":
            fntool = 'd8flowdir'
        elif globalsetting.osplatform == "Windows":
            fntool = 'D8FlowDir.exe'

        return taudemfuncs.run(fntool,
                               [('-fel', felFile)],
                               [],
                               [('-sd8', sd8File),
                                ('-p', pFile)], 
                                numProcesses, 
                                False)

    @staticmethod
    def runDinfFlowDir(felFile, slpFile, angFile, numProcesses):
        """Run DinfFlowDir."""

        if globalsetting.osplatform == "linux":
            fntool = 'dinfflowdir'
        elif globalsetting.osplatform == "Windows":
            fntool = 'DinfFlowDir.exe'

        return taudemfuncs.run(fntool,
                               [('-fel', felFile)],
                               [], 
                               [('-slp', slpFile),
                                ('-ang', angFile)],
                                numProcesses, False)

    @staticmethod
    def runAreaD8(pFile, ad8File, outletFile, weightFile,
                  numProcesses, contCheck=False, mustRun=True):
        """Run AreaD8."""
        inFiles = [('-p', pFile)]
        if outletFile is not None:
            inFiles.append(('-o', outletFile))
        if weightFile is not None:
            inFiles.append(('-wg', weightFile))
        check = [] if contCheck else [('-nc', '')]

        if globalsetting.osplatform == "linux":
            fntool = 'aread8'
        elif globalsetting.osplatform == "Windows":
            fntool = 'AreaD8.exe'

        return taudemfuncs.run(fntool, 
                               inFiles,
                               check,
                               [('-ad8', ad8File) ],
                               numProcesses,
                               mustRun)

    @staticmethod
    def runAreaDinf(angFile, scaFile, 
                    outletFile, numProcesses, mustRun=True):
        """Run AreaDinf."""
        inFiles = [('-ang', angFile)]
        if outletFile is not None:
            inFiles.append(('-o', outletFile))

        if globalsetting.osplatform == "linux":
            fntool = 'areadinf'
        elif globalsetting.osplatform == "Windows":
            fntool = 'AreaDinf.exe'

        return taudemfuncs.run(fntool,
                               inFiles,
                               [('-nc', '')],
                               [('-sca', scaFile)],
                               numProcesses, 
                               mustRun)

    @staticmethod
    def runGridNet(pFile, plenFile, tlenFile, gordFile, 
                   outletFile, numProcesses, mustRun=True):
        """Run GridNet."""
        inFiles = [('-p', pFile)]
        if outletFile is not None:
            inFiles.append(('-o', outletFile))

        if globalsetting.osplatform == "linux":
            fntool = 'gridnet'
        elif globalsetting.osplatform == "Windows":
            fntool = 'GridNet.exe'

        return taudemfuncs.run(fntool,
                               inFiles,
                               [],
                               [('-plen', plenFile),
                                ('-tlen', tlenFile), 
                                ('-gord', gordFile)],
                                numProcesses, mustRun)
    
    @staticmethod
    def runThreshold(ad8File, srcFile, threshold, numProcesses, mustRun=True):
        """Run Threshold."""
        if globalsetting.osplatform == "linux":
            fntool = 'threshold'
        elif globalsetting.osplatform == "Windows":
            fntool = 'Threshold.exe'

        return taudemfuncs.run(fntool,
                               [('-ssa', ad8File)],
                               [('-thresh', threshold)],
                               [('-src', srcFile)],
                               numProcesses,
                               mustRun)
    
    @staticmethod
    def runStreamNet(felFile, pFile, ad8File, srcFile, outletFile, 
                     ordFile, treeFile, coordFile, streamFile,
                     wFile, single, numProcesses, mustRun=True):
        """Run StreamNet."""
        inFiles = [('-fel', felFile), ('-p', pFile), ('-ad8', ad8File), ('-src', srcFile)]
        if outletFile is not None:
            inFiles.append(('-o', outletFile))
        inParms = [('-sw', '')] if single else []

        if globalsetting.osplatform == "linux":
            fntool = 'streamnet'
        elif globalsetting.osplatform == "Windows":
            fntool = 'StreamNet.exe'

        return taudemfuncs.run(fntool, inFiles, inParms, 
                               [('-ord', ordFile), ('-tree', treeFile), ('-coord', coordFile), ('-net', streamFile), ('-w', wFile)], 
                               numProcesses, mustRun)
                               
    @staticmethod
    def runMoveOutlets(pFile, srcFile, outletFile, 
                       movedOutletFile, maximumDist, numProcesses,
                       mustRun=True):
        """Run MoveOutlets."""

        if globalsetting.osplatform == "linux":
            fntool = 'moveoutletstostrm'
        elif globalsetting.osplatform == "Windows":
            fntool = 'MoveOutletsToStreams.exe'

        inFiles = [('-p', pFile), ('-src', srcFile), ('-o', outletFile)]
        inParms = [('-md', maximumDist)]
        return taudemfuncs.run(fntool, inFiles, inParms, [('-om', movedOutletFile)], 
                               numProcesses, mustRun)
        
    @staticmethod
    def runDistanceToStreams(pFile, hd8File, distFile, 
                             threshold, numProcesses, mustRun=True):
        """Run D8HDistToStrm."""
        if globalsetting.osplatform == "linux":
            fntool = 'd8hdisttostrm'
        elif globalsetting.osplatform == "Windows":
            fntool = 'D8HDistToStrm.exe'


        return taudemfuncs.run(fntool, [('-p', pFile), ('-src', hd8File)], [('-thresh', threshold)], [('-dist', distFile)], 
                               numProcesses, mustRun)     
        
        
        
        
        
    @staticmethod   
    def run(command, 
            inFiles, 
            inParms, 
            outFiles, 
            numProcesses, 
            mustRun):
        """
        Run TauDEM command, using mpiexec if numProcesses is not zero.
        
        Parameters:
        inFiles: list of pairs of parameter id (string) and file path (string) 
        for input files.  May not be empty.
        inParms: list of pairs of parameter id (string) and parameter value 
        (string) for input parameters.
        For a parameter which is a flag with no value, parameter value 
        should be empty string.
        outFiles: list of pairs of parameter id (string) and file path 
        (string) for output files.
        numProcesses: number of processes to use (int).  
        Zero means do not use mpiexec.
        output: buffer for TauDEM output (QTextEdit).
        if output is None use as flag that running in batch, and errors are simply printed.
        Return: True if no error detected, else false.
        The command is not executed if 
        (1) mustRun is false (since it is set true for results that depend 
        on the threshold setting or an outlets file, which might have changed), and
        (2) all output files exist and were last modified no earlier 
        than the first input file.
        An error is detected if any input file does not exist or,
        after running the TauDEM command, 
        any output file does not exist or was last modified earlier 
        than the first input file.
        For successful output files the .prj file is copied 
        from the first input file.
        The Taudem executable directory and the mpiexec path are 
        read from QSettings.
        """
        baseFile = inFiles[0][1]
        needToRun = mustRun
        if not needToRun:
            for (pid, fileName) in outFiles:
                if not generalfuncs.isUpToDate(baseFile, fileName):
                    needToRun = True
                    break
        if not needToRun:
            return True

        commands = []

        
        generalfuncs.addToLog('------------------- TauDEM command: -------------------\n')
        if numProcesses != 0:
            mpiexecPath = globalsetting.mpiexecPath
            if mpiexecPath != '':
                commands.append(mpiexecPath)
                commands.append('-np') # -n acceptable in Windows but only -np in OpenMPI
                commands.append(str(numProcesses))

        commands.append(os.path.join(globalsetting.fdtaudembin,
                                command))
               
        for (pid, fileName) in inFiles:
            if not pathlib.Path(fileName).exists():
                print("File does not exist: %s." %(fileName))
                return False
            commands.append(pid)
            commands.append(fileName)
        for (pid, parm) in inParms:
            commands.append(pid)
            # allow for parameter which is flag with no value
            if not parm == '':
                commands.append(parm)
        for (pid, fileName) in outFiles:
            commands.append(pid)
            commands.append(fileName)


        if globalsetting.osplatform == "linux":
            commands = " ".join(commands)
        generalfuncs.addToLog(commands)
        print(commands)
        proc = subprocess.run(commands, shell=True, stderr=subprocess.PIPE)


        
    @staticmethod
    def checkMPIExecPath(path):
        
        """Find and return path of MPI execuatable, if any, else None."""
        if os.path.exists(path):
            return True
        else:
            return False
