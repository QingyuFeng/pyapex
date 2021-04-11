# -*- coding: utf-8 -*-
import subprocess, os
import json

from .globalsetting import globalsetting
globalsetting = globalsetting()

class graphUtil():

    def __init__(self):
        self.demo = ""

    @staticmethod
    # Read in the tree file
    def readTree(fnTree: str):

        fid = open(fnTree, 'r')
        lif = fid.readlines()
        fid.close

        treedict = {}
        
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split('\t')
            while '' in lif[lidx]:
                lif[lidx].remove('')
                
            lif[lidx][-1] = lif[lidx][-1][:-1]
            # 3: downstream
            # 4: 1st upstream
            # 5: 2nd upstream
            # 0: this stream
            
            treedict[lif[lidx][0]] = lif[lidx][3:] + [lif[lidx][0]]

        return treedict   

    @staticmethod
    def rmExtraStrm(subdemwlst, substreamdict):
        '''
        This function removed the subareas from subnoinstream
        which do not exist in subnoindemw. 
        '''
        # substrm is the list of subnumbers in the tree file
        # substrmtorm is the stream number only exists in the 
        # tree file but not in the demw files (the raster map)
        substrm = substreamdict.keys()
        
        
        substrmtorm = [i for i in substrm
                       if not i in subdemwlst]

        # Here I just removed them by reconnecting the streams       
        for subid in range(len(substrmtorm)):
#            print("processing subarea: ", subid)
            # Get the upstream and downstrema of the value to be removed
            tempvalue = None
            tempvalue = substreamdict[substrmtorm[subid]]
#            print('temo...: ',subid, tempvalue)
            
            # The streams connected by this need to be modified
            # value of dict [sub, downstrm, upstream1, upstream2]
            # upstream1 = tempvalue[2]
            
            # Change this subarea's downstream's upstream to
            # this subarea's downstream
            # There are two upstreams.
            # Since we are removing, and the upstreams will have 
            # a downstream, which is the one to be removed. This downstream
            # will be changed to the to-be-removed stream's downstream 
            # to make the connection. 
            # index 0 is downstream
#            print('upstream1: ',tempvalue[1],substreamdict[tempvalue[1]])
            substreamdict[tempvalue[1]][0] = tempvalue[0]
#            print('upstream1 lat: ', tempvalue[1],substreamdict[tempvalue[1]])
            
#            print('upstream2...: ',tempvalue[2],substreamdict[tempvalue[2]])
            substreamdict[tempvalue[2]][0] = tempvalue[0]
#            print('upstream2 lat: ', tempvalue[2], substreamdict[tempvalue[2]])

            # Change the upstream of this subarea's downstream to
            # its first upstream
            # The downstream might have two upstream, only change the one
            # that is equal to the subarea to be removed.
#            print('downstream', tempvalue[0], substreamdict[tempvalue[0]][1])
#            print('downstream', tempvalue[0], substreamdict[tempvalue[0]][2])
            
            if (substreamdict[tempvalue[0]][1] == substrmtorm[subid]):
#                print('upstream1: ',substreamdict[tempvalue[0]])
                substreamdict[tempvalue[0]][1] = tempvalue[1]
#                print('upstream1 later: ',substreamdict[tempvalue[0]])
            elif (substreamdict[tempvalue[0]][2] == substrmtorm[subid]):
#                print('upstream2: ',substreamdict[tempvalue[0]])
                substreamdict[tempvalue[0]][2] = tempvalue[1]
#                print('upstream2 later: ',substreamdict[tempvalue[0]])
            
            # First remove keys in dict
            substreamdict.pop(substrmtorm[subid], None)
            # First remove keys in dict
            substreamdict.pop(subid, None)

        return substreamdict




    @staticmethod
    def graphForWS(treedict):
        '''
        represent the watershed using a unreachable graph
        wsGraph = {node: [neighbors]}
        '''
        wsGraph = {}

        for key, value in treedict.items():
            wsGraph[key] = [k for k, v in treedict.items()
                            if v[0] == key]
            
        return wsGraph


    @staticmethod
    def getOutletSubsUsrBdy(subinfld, treedict):
        '''
        This function will loop through each sub no in field,
        find its downstream no and determine whether the downstream
        is in the field. If not, the downstream will be determined as
        a watershed outlet subarea.
        '''
        outletlist = []

        for subid in subinfld:
            if not treedict[subid][0] in subinfld:
                if not subid in outletlist:
                    outletlist.append(subid)
                    #print(subid, treedict[subid][0])
        return outletlist


    def groupSubstoWatersheds(self, watershedGraph, fieldOutletSubs):
        '''
        This function will loop through the outlet list and
        find the corresponding watersheds using depthfirst search
        algorithm.
        '''
        subsinWS = {}
        wsOutlets = {}
        
        # there might be some disruption of numbers, 
        # making the ws no not continuous.
        # I add a counter, ever time, there need to be
        # one append, add one.
        wsctr = 0
        for olid in range(len(fieldOutletSubs)):
            subPurePath = self.dfs_iterative(
                                    watershedGraph,
                                    fieldOutletSubs[olid])       
            # Jusge whether the new watershed is contained
            # in the old paths
            if olid == 0:
                wsctr = wsctr + 1
                subsinWS[wsctr] = subPurePath
                wsOutlets[wsctr] = fieldOutletSubs[olid]
            else:
                newpathlen = len(subPurePath)
                for k, v in subsinWS.items():
                    vlen = 0
                    vlen = len(v)
                    if vlen >= newpathlen:
                        if not set(subPurePath).issubset(set(v)):
                            # This means the new one is the subset of the existing one,
                            wsctr = wsctr + 1
                            subsinWS[wsctr] = subPurePath
                            wsOutlets[wsctr] = fieldOutletSubs[olid]
                            break
                        else:
                            break
                    elif vlen < newpathlen:
                        if set(v).issubset(set(subPurePath)):
                            # This means the existing one is the subset of the new one:
                            # replace it with the new one
                            subsinWS[k] = subPurePath
                            wsOutlets[k] = fieldOutletSubs[k]
                            break
                        else:
                            wsctr = wsctr + 1
                            subsinWS[wsctr] = subPurePath
                            wsOutlets[wsctr] = fieldOutletSubs[olid]
                            break

        return subsinWS


    def dfs_iterative(self, graph, start):
        stack, path = [start], []

        while stack:
            vertex = stack.pop()
            if vertex in path:
                continue
            path.append(vertex)
            for neighbor in graph[vertex]:
                stack.append(neighbor)

        return path


    def removeExtraWS(self, wssubdict):
            
        # This function was written to remove single subareas already
        # contained in other watersheds.
        # The steps include: 
        # 1. Construct a list ordered by length of watershed subarea numbers.
        # 2. Construct a list of watershed only have 1 subareas.
        # 3. Loop through each of the first list, if the one subarea is
        # found in one larger watershed, remove the subarea from the list.
        wslist = sorted([v for k, v in wssubdict.items()], key=len, reverse=True)
        
        singlesublist = [v for k, v in wssubdict.items() if (len(v) == 1)]
        
        subtobepoped = []
        
        for wsid in wslist:
            if len(wsid) > 1:
                for subno in singlesublist:
                    if subno[0] in wsid:
                        subtobepoped.append(subno[0])

        for rmid in subtobepoped:
            if rmid in wslist:
                wslist.remove([rmid])
            
        # Create a new dictionary
        wsdict = {}
        
        for wsid2 in range(len(wslist)):
            wsdict[wsid2+1] = wslist[wsid2]
        
        return wsdict



    def reclassifyWsBdy(self, wssubdict, fdReclassifiedWS, 
        fnGdalReclassPy, fullsubWSFile, fnpSubRecPair):
        '''
        Loop throught each watershed and reclassify the demw.
        '''
        reclassPairs = {}
        for key,value in wssubdict.items():
            if (len(value)> 0):
                # Reclassify the demw
                reclassPairs[key] = self.reclassify(key, value, 
                    fdReclassifiedWS, fnGdalReclassPy, fullsubWSFile)
        
        # Write the information into json files
        with open(fnpSubRecPair, 'w') as fp:
            json.dump(reclassPairs, fp)

        return reclassPairs

            

    def reclassify(self, wsno, wssubids, 
            fdReclassifiedWS, fnGdalReclassPy, fullsubWSFile):

        """
        # gdal_reclassify.py [-c source_classes] [-r dest_classes]
        # [-d default] [-n default_as_nodata] src_dataset dst_dataset

        Example of using the tool:
        python gdal_reclassify.py source_dataset.tif
         destination_dataset.tif -c "<30, <50, <80, ==130, <210"
        -r "1, 2, 3, 4, 5" -d 0 -n true -p "COMPRESS=LZW"

        Steps include:
            1. generate the source classes
            2. generate the dest_classes
            3. generate the command
            4. run the command
        """
        # Storing the original and reclassified subarea numbers
        # This will have two elements as lists: the original (src_classes),
        # the new (des_classes1)
        reclasspair = []

        # used to construct commands
        src_classes = []
        # used for appending to reclasspair
        src_classes_store = []
        # des_classes: for display: I will reclassify
        # the subareas into 1 to max. This is because
        # mapserver is hard to handle 32 bit raster.
        # I will try with 24 bit or 16 bit later.
        # But here let's work on the 8 bit first.
        des_classes1 = []

        # I will create two reclass layers for display
        # The one des_classes1 contains new numbers, these will
        # be converted to subarea shapefiles.
        # des_classes2 will only be one number for the watershed.
        des_classes2 = []
        for subid in range(len(wssubids)):
            src_classes.append("==" + wssubids[subid])
            src_classes_store.append(wssubids[subid])
            des_classes1.append(subid+1)
            des_classes2.append(wsno)

        reclasspair.append(src_classes_store)
        reclasspair.append(des_classes1)

        src_classes = ",".join(src_classes)
        des_classes1 = ",".join(map(str, des_classes1))

        # output DEMREC name
        outrecdemw1 = os.path.join(
                    fdReclassifiedWS,
                    'recws%i.tif' %(wsno)) 
        #indemwtif = fin_demw
        
        # Then generate command
        commands = ['python',
                fnGdalReclassPy,
                fullsubWSFile,
                outrecdemw1,
                '-c',
                src_classes,
                '-r',
                des_classes1,
                '-d',
                '0',
                '-n',
                'true']
        # cmd1 = ['python '
        #         + fnGdalReclassPy
        #         + ' '
        #        + fullsubWSFile
        #        + ' '
        #        + outrecdemw1
        #        + ' -c "'
        #        + src_classes
        #        + '" -r "'
        #        + des_classes1
        #        + '" -d 0 -n true']
#        print(cmd1)
        if globalsetting.osplatform == "linux":
            commands = " ".join(commands)
        # print(commands)
        proc = subprocess.run(commands, shell=True, stderr=subprocess.PIPE)

        # p = subprocess.run(cmd1[0], shell=True, stderr=subprocess.PIPE)

        des_classes2 = ",".join(map(str, des_classes2))

        # output DEMREC name
        outrecdemw2 = os.path.join(
                    fdReclassifiedWS,
                    'wsnorecws%i.tif' %(wsno)) 
        
        # Then generate command
        # cmd2 = ['python '
        #         + fnGdalReclassPy
        #         + ' '
        #        + fullsubWSFile
        #        + ' '
        #        + outrecdemw2
        #        + ' -c "'
        #        + src_classes
        #        + '" -r "'
        #        + des_classes2
        #        + '" -d 0 -n true']

        commands = ['python',
                fnGdalReclassPy,
                fullsubWSFile,
                outrecdemw2,
                '-c',
                src_classes,
                '-r',
                des_classes2,
                '-d',
                '0',
                '-n',
                'true']
        if globalsetting.osplatform == "linux":
            commands = " ".join(commands)
        # print(commands)
        proc = subprocess.run(commands, shell=True, stderr=subprocess.PIPE)

        # p = subprocess.run(cmd2[0], shell=True, stderr=subprocess.PIPE)

        return reclasspair
