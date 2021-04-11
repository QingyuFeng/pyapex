# -*- coding: utf-8 -*-
import os
import subprocess
import pandas as pd
import datetime
import sqlite3


from .generalfuncs import generalfuncs
generalfuncs = generalfuncs()


class climfuncs():
    """Various utilities."""

    @staticmethod
    def getCliNearStn(longitude: float, 
                    latitude: float, 
                    fdapexrun: str, 
                    fnclimsearexe: str,
                    fnclimstndb: str):
        
        """
        Search the nearest climate station by latitude and longitude
        using a c++ program. 
        """
        # Generate the commands to run the commands
        # "/climNearest.exe $ziplong $ziplat $rundir $weastnlist"        
        procCommand = ['%s %f %f %s/ %s' %(
                    fnclimsearexe,
                    longitude,
                    latitude,
                    fdapexrun,
                    fnclimstndb
                    )]
        generalfuncs.addToLog(procCommand)

        p = subprocess.run(procCommand[0], stdout=subprocess.PIPE, shell=True)
        

    @staticmethod
    def getFoundStnInfo(fnoutstn: str):

        # Get the content of the output station files
        fid = open(fnoutstn, 'r')
        lif = fid.readlines()
        fid.close()  
        
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx][:-1]
        
        return lif

    
    @staticmethod
    def readweastndb2dict(fninstndb: str):

        # Get the content of the output station files
        fid = open(fninstndb, 'r')
        lif = fid.readlines()
        fid.close()  
        
        lifdict = {}

        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split(";")
            lifdict[lif[lidx][1][1:-1]] = lif[lidx][2:]

        return lifdict

    
    @staticmethod
    def writeapexcom(fncom: str,
                        stninfodb: dict,
                        stnlist: str,
                        fileextension: str
                        ):

        # Open file for write written
        if os.path.isfile(fncom):
            os.remove(fncom)
                                
        outfidcom = None
        outfidcom = open(fncom, "w")

        for wstnidx in range(len(stnlist)):
            # Write each station
            # Stninfo format:
            # key: station name
            # value: [stnno, lat, long, runyear, elev]
            # Com file format
            # ID, name.extension, lat, long, ST, Loc
            stnname = None
            stnname = stnlist[wstnidx]
            outfidcom.writelines("%5i\t%s.%s\t%5.3f\t%5.3f\t%10s\t%s\n"
                        %(wstnidx+1,
                        stnname,
                        fileextension,
                        float(stninfodb[stnname][1]),
                        float(stninfodb[stnname][2]),
                        "NA",
                        stnname
                        ))

        outfidcom.close()


    @staticmethod
    def writewp1file(fnDbSolCli: str,
                    stationname: str,
                    fdapexrun: str,
                    wgntablename: str
                    ):

        sqlconn = None
        try:
            sqlconn = sqlite3.connect(fnDbSolCli)
        except sqlite3.Error as e:
            print(e)

        sqlstmt = "SELECT * FROM %s where stationname = '%s'" %(
                                    wgntablename,
                                    stationname)

        Result = pd.read_sql(sqlstmt, con=sqlconn)

        if sqlconn is not None:
            sqlconn.close()

        # Open a file for writing
        """
        READ(KR(K),'(A10)')TMPSTR
        READ(KR(K),FMT)(OBMX(IWI,I),I=1,12)
        READ(KR(K),FMT)(OBMN(IWI,I),I=1,12)
        READ(KR(K),FMT)(SDTMX(IWI,I),I=1,12)
        READ(KR(K),FMT)(SDTMN(IWI,I),I=1,12)
        READ(KR(K),FMT)(RMO(IWI,I),I=1,12)
        READ(KR(K),FMT)(RST(2,IWI,I),I=1,12)
        READ(KR(K),FMT)(RST(3,IWI,I),I=1,12)
        READ(KR(K),FMT)(PRW(1,IWI,I),I=1,12)
        READ(KR(K),FMT)(PRW(2,IWI,I),I=1,12)
        READ(KR(K),FMT)(UAVM(I),I=1,12)
        READ(KR(K),FMT)(WI(IWI,I),I=1,12)
        READ(KR(K),FMT)(OBSL(IWI,I),I=1,12)
        READ(KR(K),FMT)(RH(IWI,I),I=1,12)
        READ(KR(K),FMT)(UAV0(I),I=1,12)
        """
        fnwp1 = os.path.join(
            fdapexrun,
            "%s.WP1" %(stationname)
        )
        if os.path.exists(fnwp1):
            os.remove(fnwp1)

        fid = open(fnwp1, "w")

        # Create line for writing

        fid.writelines("    LAT = %7.2f   LON =   %7.2f    ELEV = %7.2f     \n" %(
            Result.loc[0, "latitude"],
            Result.loc[0, "longitude"],
            Result.loc[0, "elevation"]
            ))

        fid.writelines("%s\n" %(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")))
        
        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "obmxmon1"],
            Result.loc[0, "obmxmon2"],
            Result.loc[0, "obmxmon3"],
            Result.loc[0, "obmxmon4"],
            Result.loc[0, "obmxmon5"],
            Result.loc[0, "obmxmon6"],
            Result.loc[0, "obmxmon7"],
            Result.loc[0, "obmxmon8"],
            Result.loc[0, "obmxmon9"],
            Result.loc[0, "obmxmon10"],
            Result.loc[0, "obmxmon11"],
            Result.loc[0, "obmxmon12"]
            ))
					
        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "obmnmon1"],
            Result.loc[0, "obmnmon2"],
            Result.loc[0, "obmnmon3"],
            Result.loc[0, "obmnmon4"],
            Result.loc[0, "obmnmon5"],
            Result.loc[0, "obmnmon6"],
            Result.loc[0, "obmnmon7"],
            Result.loc[0, "obmnmon8"],
            Result.loc[0, "obmnmon9"],
            Result.loc[0, "obmnmon10"],
            Result.loc[0, "obmnmon11"],
            Result.loc[0, "obmnmon12"]
            ))

        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "stdmxmon1"],
            Result.loc[0, "stdmxmon2"],
            Result.loc[0, "stdmxmon3"],
            Result.loc[0, "stdmxmon4"],
            Result.loc[0, "stdmxmon5"],
            Result.loc[0, "stdmxmon6"],
            Result.loc[0, "stdmxmon7"],
            Result.loc[0, "stdmxmon8"],
            Result.loc[0, "stdmxmon9"],
            Result.loc[0, "stdmxmon10"],
            Result.loc[0, "stdmxmon11"],
            Result.loc[0, "stdmxmon12"]
            ))

        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "stdmnmon1"],
            Result.loc[0, "stdmnmon2"],
            Result.loc[0, "stdmnmon3"],
            Result.loc[0, "stdmnmon4"],
            Result.loc[0, "stdmnmon5"],
            Result.loc[0, "stdmnmon6"],
            Result.loc[0, "stdmnmon7"],
            Result.loc[0, "stdmnmon8"],
            Result.loc[0, "stdmnmon9"],
            Result.loc[0, "stdmnmon10"],
            Result.loc[0, "stdmnmon11"],
            Result.loc[0, "stdmnmon12"]
            ))

        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "rmomon1"],
            Result.loc[0, "rmomon2"],
            Result.loc[0, "rmomon3"],
            Result.loc[0, "rmomon4"],
            Result.loc[0, "rmomon5"],
            Result.loc[0, "rmomon6"],
            Result.loc[0, "rmomon7"],
            Result.loc[0, "rmomon8"],
            Result.loc[0, "rmomon9"],
            Result.loc[0, "rmomon10"],
            Result.loc[0, "rmomon11"],
            Result.loc[0, "rmomon12"]
            ))

        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "rst2mon1"],
            Result.loc[0, "rst2mon2"],
            Result.loc[0, "rst2mon3"],
            Result.loc[0, "rst2mon4"],
            Result.loc[0, "rst2mon5"],
            Result.loc[0, "rst2mon6"],
            Result.loc[0, "rst2mon7"],
            Result.loc[0, "rst2mon8"],
            Result.loc[0, "rst2mon9"],
            Result.loc[0, "rst2mon10"],
            Result.loc[0, "rst2mon11"],
            Result.loc[0, "rst2mon12"]
            ))

        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "rst3mon1"],
            Result.loc[0, "rst3mon2"],
            Result.loc[0, "rst3mon3"],
            Result.loc[0, "rst3mon4"],
            Result.loc[0, "rst3mon5"],
            Result.loc[0, "rst3mon6"],
            Result.loc[0, "rst3mon7"],
            Result.loc[0, "rst3mon8"],
            Result.loc[0, "rst3mon9"],
            Result.loc[0, "rst3mon10"],
            Result.loc[0, "rst3mon11"],
            Result.loc[0, "rst3mon12"]
            ))


        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "prw1mon1"],
            Result.loc[0, "prw1mon2"],
            Result.loc[0, "prw1mon3"],
            Result.loc[0, "prw1mon4"],
            Result.loc[0, "prw1mon5"],
            Result.loc[0, "prw1mon6"],
            Result.loc[0, "prw1mon7"],
            Result.loc[0, "prw1mon8"],
            Result.loc[0, "prw1mon9"],
            Result.loc[0, "prw1mon10"],
            Result.loc[0, "prw1mon11"],
            Result.loc[0, "prw1mon12"]
            ))


        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "prw2mon1"],
            Result.loc[0, "prw2mon2"],
            Result.loc[0, "prw2mon3"],
            Result.loc[0, "prw2mon4"],
            Result.loc[0, "prw2mon5"],
            Result.loc[0, "prw2mon6"],
            Result.loc[0, "prw2mon7"],
            Result.loc[0, "prw2mon8"],
            Result.loc[0, "prw2mon9"],
            Result.loc[0, "prw2mon10"],
            Result.loc[0, "prw2mon11"],
            Result.loc[0, "prw2mon12"]
            ))

        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "uavmmon1"],
            Result.loc[0, "uavmmon2"],
            Result.loc[0, "uavmmon3"],
            Result.loc[0, "uavmmon4"],
            Result.loc[0, "uavmmon5"],
            Result.loc[0, "uavmmon6"],
            Result.loc[0, "uavmmon7"],
            Result.loc[0, "uavmmon8"],
            Result.loc[0, "uavmmon9"],
            Result.loc[0, "uavmmon10"],
            Result.loc[0, "uavmmon11"],
            Result.loc[0, "uavmmon12"]
            ))

        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "wimon1"],
            Result.loc[0, "wimon2"],
            Result.loc[0, "wimon3"],
            Result.loc[0, "wimon4"],
            Result.loc[0, "wimon5"],
            Result.loc[0, "wimon6"],
            Result.loc[0, "wimon7"],
            Result.loc[0, "wimon8"],
            Result.loc[0, "wimon9"],
            Result.loc[0, "wimon10"],
            Result.loc[0, "wimon11"],
            Result.loc[0, "wimon12"]
            ))

        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "obslmon1"],
            Result.loc[0, "obslmon2"],
            Result.loc[0, "obslmon3"],
            Result.loc[0, "obslmon4"],
            Result.loc[0, "obslmon5"],
            Result.loc[0, "obslmon6"],
            Result.loc[0, "obslmon7"],
            Result.loc[0, "obslmon8"],
            Result.loc[0, "obslmon9"],
            Result.loc[0, "obslmon10"],
            Result.loc[0, "obslmon11"],
            Result.loc[0, "obslmon12"]
            ))

        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "rhmon1"],
            Result.loc[0, "rhmon2"],
            Result.loc[0, "rhmon3"],
            Result.loc[0, "rhmon4"],
            Result.loc[0, "rhmon5"],
            Result.loc[0, "rhmon6"],
            Result.loc[0, "rhmon7"],
            Result.loc[0, "rhmon8"],
            Result.loc[0, "rhmon9"],
            Result.loc[0, "rhmon10"],
            Result.loc[0, "rhmon11"],
            Result.loc[0, "rhmon12"]
            ))

        fid.writelines("%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f%10.2f\n" %(
            Result.loc[0, "uav0mon1"],
            Result.loc[0, "uav0mon2"],
            Result.loc[0, "uav0mon3"],
            Result.loc[0, "uav0mon4"],
            Result.loc[0, "uav0mon5"],
            Result.loc[0, "uav0mon6"],
            Result.loc[0, "uav0mon7"],
            Result.loc[0, "uav0mon8"],
            Result.loc[0, "uav0mon9"],
            Result.loc[0, "uav0mon10"],
            Result.loc[0, "uav0mon11"],
            Result.loc[0, "uav0mon12"]
            ))

        fid.close()


    # TODO
    # Here we do not have observed wind distribution data and this time
    # A dummy wind data will be written to make the model run. 
    # This will not affect simulation result if we do not consider
    # wind erosion simulation. 
    @staticmethod
    def writewndfile(sqlconn: str,
                    stationname: str,
                    fdapexrun: str,
                    wgntablename: str
                    ):
        
        # sqlstmt = "SELECT * FROM %s where stationname = '%s'" %(
        #                             wgntablename,
        #                             stationname)

        # Result = pd.read_sql(sqlstmt, con=sqlconn)

        # Open a file for writing
        fnwnd = os.path.join(
            fdapexrun,
            "%s.WND" %(stationname)
        )
        if os.path.exists(fnwnd):
            os.remove(fnwnd)

        fid = open(fnwnd, "w")

        # Create line for writing

        fid.writelines("  DUMMY Wind station data \n")

        fid.writelines("%s\n" %(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")))
        
        fid.writelines("  4.68  4.78  5.11  5.15  4.55  4.46  4.16  3.81  3.56  3.81  4.34  4.41\n")
        fid.writelines(" 14.00 12.00 11.00  8.00  6.00  3.00  2.00  2.00  8.00 11.00 13.00 11.00\n")
        fid.writelines("  5.00  6.00  6.00  5.00  3.00  2.00  1.00  2.00  6.00  5.00  5.00  4.00\n")
        fid.writelines("  3.00  4.00  4.00  4.00  3.00  3.00  2.00  4.00  8.00  5.00  4.00  3.00\n")
        fid.writelines("  2.00  3.00  3.00  3.00  3.00  2.00  2.00  3.00  6.00  3.00  2.00  1.00\n")
        fid.writelines("  2.00  4.00  4.00  3.00  4.00  4.00  3.00  5.00  7.00  4.00  2.00  2.00\n")
        fid.writelines("  2.00  3.00  3.00  4.00  5.00  4.00  4.00  6.00  6.00  4.00  2.00  2.00\n")
        fid.writelines("  6.00  7.00  8.00 11.00 13.00 14.00 13.00 13.00 11.00 10.00  6.00  6.00\n")
        fid.writelines(" 10.00 10.00 13.00 20.00 22.00 24.00 22.00 19.00 13.00 14.00 12.00 10.00\n")
        fid.writelines(" 18.00 14.00 18.00 20.00 23.00 28.00 30.00 26.00 17.00 17.00 19.00 18.00\n")
        fid.writelines("  8.00  6.00  6.00  5.00  5.00  7.00 12.00 10.00  5.00  6.00  7.00  7.00\n")
        fid.writelines("  4.00  4.00  3.00  2.00  2.00  3.00  4.00  5.00  3.00  3.00  4.00  5.00\n")
        fid.writelines("  3.00  2.00  2.00  1.00  1.00  1.00  2.00  1.00  1.00  1.00  2.00  3.00\n")
        fid.writelines("  3.00  3.00  3.00  2.00  1.00  1.00  1.00  1.00  1.00  2.00  3.00  4.00\n")
        fid.writelines("  3.00  3.00  3.00  2.00  2.00  1.00   .00  1.00  1.00  2.00  3.00  3.00\n")
        fid.writelines("  7.00  7.00  5.00  4.00  3.00  1.00  1.00  1.00  3.00  5.00  7.00 10.00\n")
        fid.writelines(" 11.00 10.00  8.00  6.00  3.00  2.00  1.00  1.00  4.00  7.00 10.00 12.00\n")

        fid.close()
        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "obmxmon1"],
        #     Result.loc[0, "obmxmon2"],
        #     Result.loc[0, "obmxmon3"],
        #     Result.loc[0, "obmxmon4"],
        #     Result.loc[0, "obmxmon5"],
        #     Result.loc[0, "obmxmon6"],
        #     Result.loc[0, "obmxmon7"],
        #     Result.loc[0, "obmxmon8"],
        #     Result.loc[0, "obmxmon9"],
        #     Result.loc[0, "obmxmon10"],
        #     Result.loc[0, "obmxmon11"],
        #     Result.loc[0, "obmxmon12"]
        #     ))
					
        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "obmnmon1"],
        #     Result.loc[0, "obmnmon2"],
        #     Result.loc[0, "obmnmon3"],
        #     Result.loc[0, "obmnmon4"],
        #     Result.loc[0, "obmnmon5"],
        #     Result.loc[0, "obmnmon6"],
        #     Result.loc[0, "obmnmon7"],
        #     Result.loc[0, "obmnmon8"],
        #     Result.loc[0, "obmnmon9"],
        #     Result.loc[0, "obmnmon10"],
        #     Result.loc[0, "obmnmon11"],
        #     Result.loc[0, "obmnmon12"]
        #     ))

        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "stdmxmon1"],
        #     Result.loc[0, "stdmxmon2"],
        #     Result.loc[0, "stdmxmon3"],
        #     Result.loc[0, "stdmxmon4"],
        #     Result.loc[0, "stdmxmon5"],
        #     Result.loc[0, "stdmxmon6"],
        #     Result.loc[0, "stdmxmon7"],
        #     Result.loc[0, "stdmxmon8"],
        #     Result.loc[0, "stdmxmon9"],
        #     Result.loc[0, "stdmxmon10"],
        #     Result.loc[0, "stdmxmon11"],
        #     Result.loc[0, "stdmxmon12"]
        #     ))

        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "stdmnmon1"],
        #     Result.loc[0, "stdmnmon2"],
        #     Result.loc[0, "stdmnmon3"],
        #     Result.loc[0, "stdmnmon4"],
        #     Result.loc[0, "stdmnmon5"],
        #     Result.loc[0, "stdmnmon6"],
        #     Result.loc[0, "stdmnmon7"],
        #     Result.loc[0, "stdmnmon8"],
        #     Result.loc[0, "stdmnmon9"],
        #     Result.loc[0, "stdmnmon10"],
        #     Result.loc[0, "stdmnmon11"],
        #     Result.loc[0, "stdmnmon12"]
        #     ))

        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "rmomon1"],
        #     Result.loc[0, "rmomon2"],
        #     Result.loc[0, "rmomon3"],
        #     Result.loc[0, "rmomon4"],
        #     Result.loc[0, "rmomon5"],
        #     Result.loc[0, "rmomon6"],
        #     Result.loc[0, "rmomon7"],
        #     Result.loc[0, "rmomon8"],
        #     Result.loc[0, "rmomon9"],
        #     Result.loc[0, "rmomon10"],
        #     Result.loc[0, "rmomon11"],
        #     Result.loc[0, "rmomon12"]
        #     ))

        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "rst2mon1"],
        #     Result.loc[0, "rst2mon2"],
        #     Result.loc[0, "rst2mon3"],
        #     Result.loc[0, "rst2mon4"],
        #     Result.loc[0, "rst2mon5"],
        #     Result.loc[0, "rst2mon6"],
        #     Result.loc[0, "rst2mon7"],
        #     Result.loc[0, "rst2mon8"],
        #     Result.loc[0, "rst2mon9"],
        #     Result.loc[0, "rst2mon10"],
        #     Result.loc[0, "rst2mon11"],
        #     Result.loc[0, "rst2mon12"]
        #     ))

        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "rst3mon1"],
        #     Result.loc[0, "rst3mon2"],
        #     Result.loc[0, "rst3mon3"],
        #     Result.loc[0, "rst3mon4"],
        #     Result.loc[0, "rst3mon5"],
        #     Result.loc[0, "rst3mon6"],
        #     Result.loc[0, "rst3mon7"],
        #     Result.loc[0, "rst3mon8"],
        #     Result.loc[0, "rst3mon9"],
        #     Result.loc[0, "rst3mon10"],
        #     Result.loc[0, "rst3mon11"],
        #     Result.loc[0, "rst3mon12"]
        #     ))


        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "prw1mon1"],
        #     Result.loc[0, "prw1mon2"],
        #     Result.loc[0, "prw1mon3"],
        #     Result.loc[0, "prw1mon4"],
        #     Result.loc[0, "prw1mon5"],
        #     Result.loc[0, "prw1mon6"],
        #     Result.loc[0, "prw1mon7"],
        #     Result.loc[0, "prw1mon8"],
        #     Result.loc[0, "prw1mon9"],
        #     Result.loc[0, "prw1mon10"],
        #     Result.loc[0, "prw1mon11"],
        #     Result.loc[0, "prw1mon12"]
        #     ))


        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "prw2mon1"],
        #     Result.loc[0, "prw2mon2"],
        #     Result.loc[0, "prw2mon3"],
        #     Result.loc[0, "prw2mon4"],
        #     Result.loc[0, "prw2mon5"],
        #     Result.loc[0, "prw2mon6"],
        #     Result.loc[0, "prw2mon7"],
        #     Result.loc[0, "prw2mon8"],
        #     Result.loc[0, "prw2mon9"],
        #     Result.loc[0, "prw2mon10"],
        #     Result.loc[0, "prw2mon11"],
        #     Result.loc[0, "prw2mon12"]
        #     ))

        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "uavmmon1"],
        #     Result.loc[0, "uavmmon2"],
        #     Result.loc[0, "uavmmon3"],
        #     Result.loc[0, "uavmmon4"],
        #     Result.loc[0, "uavmmon5"],
        #     Result.loc[0, "uavmmon6"],
        #     Result.loc[0, "uavmmon7"],
        #     Result.loc[0, "uavmmon8"],
        #     Result.loc[0, "uavmmon9"],
        #     Result.loc[0, "uavmmon10"],
        #     Result.loc[0, "uavmmon11"],
        #     Result.loc[0, "uavmmon12"]
        #     ))

        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "wimon1"],
        #     Result.loc[0, "wimon2"],
        #     Result.loc[0, "wimon3"],
        #     Result.loc[0, "wimon4"],
        #     Result.loc[0, "wimon5"],
        #     Result.loc[0, "wimon6"],
        #     Result.loc[0, "wimon7"],
        #     Result.loc[0, "wimon8"],
        #     Result.loc[0, "wimon9"],
        #     Result.loc[0, "wimon10"],
        #     Result.loc[0, "wimon11"],
        #     Result.loc[0, "wimon12"]
        #     ))

        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "obslmon1"],
        #     Result.loc[0, "obslmon2"],
        #     Result.loc[0, "obslmon3"],
        #     Result.loc[0, "obslmon4"],
        #     Result.loc[0, "obslmon5"],
        #     Result.loc[0, "obslmon6"],
        #     Result.loc[0, "obslmon7"],
        #     Result.loc[0, "obslmon8"],
        #     Result.loc[0, "obslmon9"],
        #     Result.loc[0, "obslmon10"],
        #     Result.loc[0, "obslmon11"],
        #     Result.loc[0, "obslmon12"]
        #     ))

        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "rhmon1"],
        #     Result.loc[0, "rhmon2"],
        #     Result.loc[0, "rhmon3"],
        #     Result.loc[0, "rhmon4"],
        #     Result.loc[0, "rhmon5"],
        #     Result.loc[0, "rhmon6"],
        #     Result.loc[0, "rhmon7"],
        #     Result.loc[0, "rhmon8"],
        #     Result.loc[0, "rhmon9"],
        #     Result.loc[0, "rhmon10"],
        #     Result.loc[0, "rhmon11"],
        #     Result.loc[0, "rhmon12"]
        #     ))

        # fid.writelines("%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f%6.2f\n" %(
        #     Result.loc[0, "uav0mon1"],
        #     Result.loc[0, "uav0mon2"],
        #     Result.loc[0, "uav0mon3"],
        #     Result.loc[0, "uav0mon4"],
        #     Result.loc[0, "uav0mon5"],
        #     Result.loc[0, "uav0mon6"],
        #     Result.loc[0, "uav0mon7"],
        #     Result.loc[0, "uav0mon8"],
        #     Result.loc[0, "uav0mon9"],
        #     Result.loc[0, "uav0mon10"],
        #     Result.loc[0, "uav0mon11"],
        #     Result.loc[0, "uav0mon12"]
        #     ))
