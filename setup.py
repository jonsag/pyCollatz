#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys, getopt

from getpass import getpass

from modules import (onError, usage, 
                     dbHost, dbName, dbUser, dbPass)
        
from db import dbConnect, createCursor, commitToDB, closeCursor, dbDisconnect, doQuery, doQueryNoPh

    
def createDB(curs, verbose):
    #dbName = "mysql"
    
    if verbose:
        print("\n--- Creating database '" + dbName + "' ...")
        
    if databaseExist(curs, dbName, verbose):
        print("\nDatabase '" + dbName + "' exists")
        return True
    else:
        if verbose:
            print("\n--- Creating database '" + dbName+ "' ...")
             
        q = ()
        sql = ("CREATE DATABASE " + dbName)
        doQuery(curs, q, sql, True, verbose)
        commitToDB(con, verbose)
        
        if databaseExist(curs, dbName, verbose):
            print("\nCreated database '" + dbName + "'")
            return True
        else:
            return False
    
    
def databaseExist(curs, database, verbose):    
    if verbose:
        print("\n--- Checking if database '" + database + "' exists ...")
    
    q = (database, )    
    sql = """SHOW DATABASES LIKE %s"""
    result = doQuery(curs, q, sql, True, verbose)
    
    if result:
        if result[0] == database:
            if verbose:
                print("\n--- Database '" + database + "' exists")
            return True
        else:
            if verbose:
                print("\n--- Database '" + database + "' does not exist")
            return False
    else:
        if verbose:
            print("\n--- Database '" + database + "' does not exist")
        return False
    
    
def createUser(curs, verbose):
    #dbUser = "root"
    
    if userExist(curs, dbUser, verbose):
        print("\nUser '" + dbUser + "' exists")
        return True
    else:
        if verbose:
            print("\n--- Creating user '" + dbUser + "' ...")
            
        q = (dbUser, dbHost, dbPass)        
        sql = """CREATE USER %s@%s IDENTIFIED BY %s"""
        doQuery(curs, q, sql, True, verbose)
        
        q = (dbUser, dbHost)        
        sql = "GRANT ALL ON " + dbName + ".* TO %s@%s"
        doQuery(curs, q, sql, True, verbose)
        
        q = ()        
        sql = """FLUSH PRIVILEGES"""
        doQuery(curs, q, sql, True, verbose)
        
        if userExist(curs, dbUser, verbose):
            print("\nCreated user '" + dbUser + "'")
            return True
        else:
            return False
            
            
def userExist(curs, userName, verbose):    
    if verbose:
        print("\n--- Checking if user '" + userName + "' exists ...")
    
    q = (userName, )    
    sql = """SELECT User FROM user WHERE User = %s"""
    result = doQuery(curs, q, sql, True, verbose)
    
    if result:
        if result[0] == userName:
            if verbose:
                print("\n--- User '" + userName + "' exists")
            return True
        else:
            if verbose:
                print("\n--- User '" + userName + "' does not exist")
            return False
    else:
        if verbose:
            print("\n--- User '" + userName + "' does not exist")
        return False
        
        
def createTables(curs, verbose):
    if verbose:
        print("\n--- Creating tables ...")
        
    tableName = "Numbers"
    
    if tableExist(curs, tableName, verbose):
        if verbose:
            print("\nTable '" + tableName + "' exists")
        return True
    else:
        if verbose:
            print("\nCreating table '" + tableName + "' ...")

        q = ()
        sql = ("CREATE TABLE " + tableName + 
               " (number INT(30) PRIMARY KEY, highest INT(30), steps INT(30), note VARCHAR(1)")
        doQuery(curs, q, sql, True, verbose)
        
        if tableExist(curs, tableName, verbose):
            print("\nCreated table '" + tableName + "'")
            return True
        else:
            return False
        
        
def tableExist(curs, tableName, verbose):
    if verbose:
        print("\nChecking if table '" + tableName + "' exists ...")
        
    q = (tableName, )    
    sql = """SHOW TABLES LIKE %s"""
    result = doQuery(curs, q, sql, True, verbose)
    
    if result:
        if result[0] == tableName:
            if verbose:
                print("\n--- Table '" + tableName + "' exists")
            return True
        else:
            if verbose:
                print("\n--- Table '" + tableName + "' does not exist")
            return False
    else:
        if verbose:
            print("\n--- Table '" + tableName + "' does not exist")
        return False
        
if __name__ == "__main__":
    setupDB = False
    con = False
    verbose = False
    
    # handle options and arguments passed to script
    try:
        myopts, args = getopt.getopt(sys.argv[1:],
                                     'svh',
                                     ['setup', 'verbose', 'help'])
    
    except getopt.GetoptError as e:
        onError(1, str(e))
    
    # if no options passed, then exit
    if len(sys.argv) == 1:  # no options passed
        onError(2, 2)
    
    # interpret options and arguments
    for option, argument in myopts:
        if option in ('-s', '--setup'):  # add connections
            setupDB = True
        elif option in ('-v', '--verbose'):  # verbose output
            verbose = True
        elif option in ('-h', '--help'):  # display help text
            usage(0)
    
    if setupDB:
        if verbose:
            print("\n--- Setting up database ...")
            
        # get root password
        print("\nEnter mysql password for user 'root'")
        while True:
            #rootPass = getpass(" ? ")
            rootPass = "plokijuh0185"
            if not rootPass:
                print("You have to type something\nTry again")
            else:
                break
            
        # connect to database mysql as root
        con = dbConnect(dbHost, "mysql", "root", rootPass, verbose)
        curs = createCursor(con, verbose)
        
        if createDB(curs, verbose):
            if createUser(curs, verbose):
                # close cursor and connection to table mysql as root
                closeCursor(curs, verbose)
                dbDisconnect(con, verbose)
                
                # connect to database collatz as collatz
                con = dbConnect(dbHost, dbName, dbUser, dbPass, verbose)
                curs = createCursor(con, verbose)
                
                if createTables(curs, verbose):
                    print("\nEverything setup successfully")
                    closeCursor(curs, verbose)
                    dbDisconnect(con, verbose)
                else:
                    onError(7, "Could not create table")
            else:
                onError(5, "Could not create user")
        else:
            onError(6, "Could not create database")
        
        
        
        
        
        
        