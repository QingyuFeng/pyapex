# -*- coding: utf-8 -*-

# Import  libraries
from .generalfuncs import generalfuncs
from .utmconversion import to_latlon, from_latlon, latlon_to_zone_number, latitude_to_zone_letter
from .utmerror import OutOfRangeError

import os
import subprocess
import json
import sys
from osgeo import gdal, ogr, osr
import numpy as np

generalfuncs = generalfuncs()


class gdalfuncs():
    """Various utilities."""
    def __init__(self):
        
        # MPI Settings:
        # If user would like to use multiprocesses to run Taudem, specify 
        # the value to desired processers.
        self.dummy = ""


    @staticmethod
    def convtif2shp(fntif: str, fnshp: str):
        procCommand = """gdal_polygonize.py -f "ESRI Shapefile"  {} {}""".format(
                fntif, fnshp) 
        generalfuncs.addToLog(procCommand)
        p = subprocess.run(procCommand, shell=True, stderr=subprocess.PIPE)

        
        
    @staticmethod
    def gdalinfostat2json(finrast: str, foutjson: str):
        """
        This function read in the raster information using gdalinfo, and write
        the output into a json file. The purpose was to get the extent of the 
        raster for larger raster clipping.
        """

        procCommand = """gdalinfo -stats -json {}""".format(finrast) 
        generalfuncs.addToLog(procCommand)
        p = subprocess.run(procCommand, shell=True, stderr=subprocess.PIPE)
        
        


    @staticmethod
    def getExtentfromJson(finjson: str):
        """
        This function the json content and return the extent from that.
        """
        jsonInfo = json.loads(open(finjson).read())
        UL = jsonInfo["cornerCoordinates"]["upperLeft"]
        LR = jsonInfo["cornerCoordinates"]["lowerRight"]
        # #For gdalwarp, the projwin should be ulx uly lrx lry
        projwin = "%s %s %s %s" %(UL[0], UL[1], LR[0], LR[1])

        return projwin


    @staticmethod
    def clipRasterbyExtent(finRas: str, finext: str, foutRas: str):
        """
        This function clips the raster by extent.
        The input of finExt is a list of loat: [minx, miny, maxx, maxy]
        """
        finext = map(str, finext)
        finext = " ".join(finext)
        procCommand = """gdal_translate -projwin {} {} {}""".format(
                                                finext,
                                                finRas,
                                                foutRas) 
        generalfuncs.addToLog(procCommand)
        p = subprocess.run(procCommand, shell=True, stderr=subprocess.PIPE)

        

    @staticmethod
    def convTif2Asc(finRas: str, foutAsc: str):
        """
        This function clips the raster by extent.
        """
        procCommand = """gdal_translate -of AAIGrid {} {}""".format(
                                                finRas,
                                                foutAsc) 
        generalfuncs.addToLog(procCommand)
        p = subprocess.run(procCommand, shell=True, stderr=subprocess.PIPE)
        return p.check_returncode()
        

    # @staticmethod
    # def getShpProjFiona(finShp: str):
    #     """
    #     This function read the projection of the shapefile in the 
    #     format of proj4.
    #     """
    #     with fiona.open(finShp) as fidShp:
    #         shpMeta = fidShp.meta

    #     spatialRef = osr.SpatialReference()
    #     """We import our WKT string into spatialRef"""
    #     spatialRef.ImportFromWkt(shpMeta["crs_wkt"])
    #     """We use the ExportToProj4() method to return a proj4 style spatial reference string."""
    #     shpSpaRefProj = spatialRef.ExportToProj4()

    #     return shpSpaRefProj
        

    @staticmethod
    def getShpProjGdal(finShp: str):
        """
        This function read the projection of the shapefile in the 
        format of proj4.
        Ref: https://pcjericks.github.io/py-gdalogr-cookbook/projection.html
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        dataset = driver.Open(finShp)
        layer = dataset.GetLayer()
        spatialRef = layer.GetSpatialRef()
        # To other formats
        # spatialRef.ExportToWkt()
        # spatialRef.ExportToPrettyWkt()
        # spatialRef.ExportToPCI()
        # spatialRef.ExportToUSGS()
        # spatialRef.ExportToXML()

        """We use the ExportToProj4() method to return a proj4 style spatial reference string."""
        shpSpaRefProj = spatialRef.ExportToProj4()

        return shpSpaRefProj


    @staticmethod
    def getRasterProj(finRaster: str):
        """
        This function read the projection of the raster (in tif now) in the 
        format of proj4.
        """
        fidRaster = gdal.Open(finRaster)
        rasterProj = fidRaster.GetProjection()

        spatialRef = osr.SpatialReference()
        """We import our WKT string into spatialRef"""
        spatialRef.ImportFromWkt(rasterProj)
        """We use the ExportToProj4() method to return a proj4 style spatial reference string."""
        spatialRefProj = spatialRef.ExportToProj4()

        return spatialRefProj


    @staticmethod
    def getRasterExtent(finRaster: str):
        """
        This function read the extent of the raster (in tif now).
        """
        fidRaster = gdal.Open(finRaster)
        # upx, xres, xskew, upy, yskew, yres = fidRaster.GetGeoTransform()
        # cols = gdalSrc.RasterXSize
        # rows = gdalSrc.RasterYSize
        
        # ulx = upx + 0*xres + 0*xskew
        # uly = upy + 0*yskew + 0*yres
        
        # llx = upx + 0*xres + rows*xskew
        # lly = upy + 0*yskew + rows*yres
        
        # lrx = upx + cols*xres + rows*xskew
        # lry = upy + cols*yskew + rows*yres
        
        # urx = upx + cols*xres + 0*xskew
        # ury = upy + cols*yskew + 0*yres

        geoTransform = fidRaster.GetGeoTransform()
        minx = geoTransform[0]
        maxy = geoTransform[3]
        maxx = minx + geoTransform[1] * fidRaster.RasterXSize
        miny = maxy + geoTransform[5] * fidRaster.RasterYSize
        return [minx, maxy, maxx, miny]




    @staticmethod
    def clipRasterbyShp(finRas: str, finShp: str, foutRas: str):
        """
        This function clips the raster by extent.
        """
        procCommand = """gdalwarp -cutline {} {} {}""".format(
                                                finShp,
                                                finRas,
                                                foutRas) 
                                    
        generalfuncs.addToLog(procCommand)
        p = subprocess.run(procCommand, shell=True, stderr=subprocess.PIPE)
        return p.check_returncode()
        

    @staticmethod
    def readASCstr(finasc):

        # Store data into a list
        data = []
        cellsize = 0.0

        # Reading files to a list 
        with open(finasc, 'r') as f:
            lif = f.read().splitlines()

        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split(' ')
            while '' in lif[lidx]:
                lif[lidx].remove('')
    
        # 0: ncols, 1: nrows, 5: NoDATA, 4: cellsize
        data.append(lif[0][1])
        data.append(lif[1][1])    
        data.append(lif[5][1])
        cellsize = float(lif[4][1])*1.0

        del(lif[:7])
        del(lif[-1])
        data.append(lif)
        # Convert 2d asc array into 1d array
        data[3] = np.asarray(data[3]).ravel()
        # Cell size is needed for area calculation
        data.append(cellsize)

        return data


    @staticmethod
    def readASCfloat(finasc):

        # Store data into a list
        data = []
        
        # Reading files to a list 
        with open(finasc, 'r') as f:
            lif = f.read().splitlines()
        # The file some times contain wrong lines.
        # TODO: check whether the value rows are the same
        # The demws.asc for dem/elevation has one more row
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split(' ')
            while '' in lif[lidx]:
                lif[lidx].remove('')

            if lidx > 5:              
                lif[lidx] = list(map(float, lif[lidx]))
        # 0: ncols, 1: nrows, 5: NoDATA, 4: cellsize
        data.append(lif[0][1])
        data.append(lif[1][1])    
        data.append(lif[5][1])
        
        #print(lif[:4])
        del(lif[:7])
        del(lif[-1])
        data.append(lif)
        # Convert 2d asc array into 1d array
        data[3] = np.asarray(data[3]).ravel()
        #print(data[3].shape)

        return data

    @staticmethod
    def readASCMode3(fileName):
        
        """
        This function read the asc files into dataframe
        """
        
        try:
            fid = open(fileName, "r")
        except:
            print("File %s does not exist!!!" %(fileName))
        
        header = []
        tmpline = []
        
        for i in range (7):
            tmpline = fid.readline()
            tmpline = tmpline.split(" ")
            while "" in tmpline:
                tmpline.remove("")
                
            tmpline[-1] = tmpline[-1][:-1]
                
            header.append(tmpline)
        
        nodata = header[-1][1]
            
        tmpline2 = ""
        data = []
        for j in range (int(header[1][1])):
            tmpline2 = fid.readline()  
            tmpline2 = tmpline2.split(" ")
            while "" in tmpline2:
                tmpline2.remove("")
            if (len(tmpline2) > 2):
                tmpline2[-1] = tmpline2[-1][:-1]
            data.append(tmpline2)
        
        fid.close()
        
        return nodata, data




    @staticmethod
    def getShpAttributes(finShp):
        '''
        Read shapefile and return all values in the
        attritube table.
        '''
        subStrAtt = dict()
        driver = ogr.GetDriverByName('ESRI Shapefile')
        dataSource = driver.Open(finShp, 0)
        layer = dataSource.GetLayer()

        # Get the field name
        '''
        According to TauDEM document for stream Reach
        and Watershed tool:
        Field names in this shapefile:
        ['0LINKNO', '1DSLINKNO', '2USLINKNO1',
        '3USLINKNO2', '4DSNODEID', '5strmOrder',
        '6Length', '7Magnitude', '8DSContArea',
        '9strmDrop', '10Slope', 'StraightL',
        'USContArea', 'WSNO', 'DOUTEND',
        'DOUTSTART', 'DOUTMID']
        * LINKNO: link number
        * DSLINKNO: downstream link, -1 indicates that this
        does not exist.
        * USLINKNO1: first upstream link
        * USLINKNO2: second upstream link
        * DSNODEID: node identifier for node at downstream
        end of each stream
        * strmOrder: strahler stream order
        * length: units are the horizontal map units of the
        underlying DEM grid
        * Magnitude: Shreve magnitude of the link. This is the
        total number of sources upstream
        * DSContArea: Drainage area at the downstream end of
        the link.
        * strmDrop: Drop in elevation from the start to the
        end of the link
        * Slope: Average slope of the link: drop/length
        * StraightL: Straight line distrance from the start
        to the end of the link
        * USContArea: Drainage area at the upstream end of
        the link
        * WSNO: Watershed NO:
        * DOUTEND: Distance to the eventual outlent from the
        downstream end of the link
        * DOUTMID: distance to the eventual outlet from the
        midpoint of the link.

        '''
        field_names = [field.name for field in layer.schema]
        # Get the value of each field for all layers
        for feature in layer:
            values_list = [str(feature.GetField(j)) for j in field_names]
            subStrAtt[str(values_list[0])] = values_list

        return subStrAtt


    def getCentroid(self, shapefile):
        '''
        Get the centroid of subarea. This was calculated from
        subarea shapefile
        '''
        subCentCoord = dict()

        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataSource = driver.Open(shapefile, 0)
        layer = dataSource.GetLayer()
        field_names = [field.name for field in layer.schema]
        # Get the value of each field for all layers
        for feature in layer:
            # There is only one field 'DN' in the shapefile.
            values_list = [feature.GetField(j) for j in field_names]
            # Now we will write the centroid co-ordinates to a text file
            # Using 'with' will close the file when the loop ends-dont need to call close
            geom = feature.GetGeometryRef()
            centroid = str([geom.Centroid().ExportToWkt()])
            # Centroid now looks like '['POINT (499702.238761793 4477029.64828273)']'
            centroid = self.CentroidStr2Float(centroid)
            centroidUtm = to_latlon(centroid[0], centroid[1], 16, 'U')
            #print(centroidUtm)
            subCentCoord[values_list[0]] = centroidUtm

        return subCentCoord

    

    def CentroidStr2Float(self, centroidStr):

        newCentroid = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in centroidStr)
        listOfNumbers = [float(i) for i in newCentroid.split()]

        return listOfNumbers

