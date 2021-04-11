# -*- coding: utf-8 -*-
import os
import json
import sqlite3



class sqldbfuncs():
    """Various utilities."""
    """Data used across across the plugin, and some utilities on it."""

    @staticmethod
    def getTableCtntfromDB(conn, tablename: str):
        
        sql2df = None
        sqlstmt = ''
        sqlstmt = "SELECT * FROM %s" %(tablename)
        sql2df = pd.read_sql(sqlstmt, con=sqlconn)
        
        return sql2df

