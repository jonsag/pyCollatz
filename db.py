#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import MySQLdb as mdb

from modules import onError

def dbConnect(dbHost, dbName, dbUser, dbPass, verbose):
    if verbose:
        print("\n--- Connecting ...\n    host: " +dbHost + 
              "\n    database: " + dbName + 
              "\n    user: " + dbUser + 
              "\n    using password " + dbPass)

    try:
        con = mdb.connect(host = dbHost, user = dbUser, passwd = dbPass, db = dbName)
    except mdb.Error as e:
        print("\nError %d: %s" % (e.args[0], e.args[1]))
        onError(3, "Could not connect to database")
    except:
        onError(4, "Could not connnect to database")
        
    return con


def dbDisconnect(con, verbose):
    if verbose:
        print("\n--- Disconnecting from database ...")
        
    con.close()
        
        
def createCursor(con, verbose):
    if verbose:
        print("\n--- Creating cursor ...")
        
    curs = con.cursor()
    
    return curs


def closeCursor(curs, verbose):
    if verbose:
        print("\n--- Closing cursor ...")
    
    curs.close()
    
        
def doQuery(curs, q, sql, single, verbose):
    if verbose:
        print("\n--- Running query: \n    '" + sql + "' % ")
        for line in q:
            print("    " + str(line))
        
    try:
        curs.execute(sql, q)
    except (mdb.Error, mdb.Warning) as e:
        print("\nError: \n" + e)
        result = ""
    else:
        if single:
            try:
                result = curs.fetchone()
            except TypeError as e:
                print("\nError: \n" + e)
            else:
                if result and verbose:
                    print("\n--- Result: \n    " + str(result))
                elif verbose:
                    print("\n--- Did not get any result")
        else:
            try:
                result = curs.fetchall()
            except TypeError as e:
                print("\nError: \n" + e)
            else:
                if result and verbose:
                    print("\n--- Result: ")
                    for line in result:
                        print("    " + line)
                elif verbose:
                    print("\n--- Did not get any result")
                    result = False
                        
    return result


def doQueryNoPh(curs, sql, single, verbose):
    if verbose:
        print("\n--- Running query: \n    '" + sql + " ...")
        
    try:
        curs.execute(sql)
    except (mdb.Error, mdb.Warning) as e:
        print("\nError: \n" + e)
        result = ""
    else:
        if single:
            try:
                result = curs.fetchone()
            except TypeError as e:
                print("\nError: \n" + e)
            else:
                if result and verbose:
                    print("\n--- Result: \n    " + result[0])
                elif verbose:
                    print("\n--- Did not get any result")
        else:
            try:
                result = curs.fetchall()
            except TypeError as e:
                print("\nError: \n" + e)
            else:
                if result and verbose:
                    print("\n--- Result: ")
                    for line in result:
                        print("    " + line)
                elif verbose:
                    print("\n--- Did not get any result")
                    result = False
                        
    return result
    
    
def commitToDB(con, verbose):
    if verbose:
        print("\n--- Committing changes to database")
        
    try:
        con.commit()
    except:
        onError(7, "Could not commit changes to database")
    else:
        return True
    
