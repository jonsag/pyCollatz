#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys, getopt

from modules import (onError, usage, 
                     dbHost, dbName, dbUser, dbPass)

from db import (dbConnect, createCursor, closeCursor, dbDisconnect, 
                doQuery, commitToDB)



def findLowestNumber(curs, verbose):
    if verbose:
        print("\n--- Finding lowest number ...")
        
    q = ()
    sql = ("SELECT min(unused) AS unused "
           "FROM ("
           "SELECT MIN(t1.number)+1 as unused "
           "FROM Numbers AS t1 WHERE NOT EXISTS (SELECT * FROM Numbers AS t2 WHERE t2.number = t1.number+1) "
           "UNION "
           #"-- Special case for missing the first row "
           "SELECT 1 "
           "FROM DUAL "
           "WHERE NOT EXISTS (SELECT * FROM Numbers WHERE number = 1)) "
           "AS subquery")
    result = doQuery(curs, q, sql, True, verbose)
    
    return result[0]

def writeToDb(number, highestNumber, steps, note, verbose):
    if verbose:
        print("\n--- Writing to database ... \n    Number: " + str(number) +
              "\n    Highest: " + str(highestNumber) +  
              " \n    Steps: " + str(steps))
        
    q = ()
    sql = ("INSERT INTO Numbers (number, highest, steps, note) VALUES (" + str(number) + 
           ", " + str(highestNumber) + 
           ", " + str(steps) + 
           ", '" + note + "')")
    result = doQuery(curs, q, sql, True, verbose)
    
    commitToDB(con, verbose)
    
def checkNumberExists(curs, number, verbose):
    if verbose:
        print("\n--- Checking if number '" + str(number) + "' exists ...")
        
    q = (number, )
    sql = ("""SELECT number, highest, steps FROM Numbers WHERE number = %s""")
    result = doQuery(curs, q, sql, True, verbose)
    
    if result:
        if verbose:
            print("\n--- Number: " + str(result[0]) + 
                  "\n    Highest: " + str(result[1]) + 
                  "\n    Steps: " + str(result[2]))
        return result[0], result[1], result[2]
    else:
        return False, False, False
    
def collatz(curs, number, verbose):
    if verbose:
        print("\n--- Running collatz calculations for entry number: " + str(number) + " ...")
    steps = 0
    highestOld = 0
    numberList = []
    
    highestNumber = number

    while number !=1:
        steps += 1
        if number% 2 == 0:
            number= number//2
            if verbose:
                print("\n--- Number is even, new number: " + str(number))

        else:
            number=  3 * number + 1
            if verbose:
                if verbose:
                    print("\n--- Number is odd, new number: " + str(number))
                
        if number > highestNumber:
            highestNumber = number 
                
        numberOld, highestOld, stepsOld = checkNumberExists(curs, number, verbose)
        
        if numberOld:
            steps = steps + stepsOld
            if highestOld > highestNumber:
                highestNumber = highestOld
            break
        else:
            if verbose:
                print("\n--- Did not appear in database "
                      "\n    Adding values to list ... "
                      "\n    Number: " + str(number) + 
                      "\n    Highest number: " + str(highestNumber) + 
                      "\n    Steps: " + str(steps))
            numberList.append((number, highestNumber, steps))
    
    if verbose:     
        print("\n--- Number is now 1")
            
    return highestNumber, steps, numberList

# add 1 to step counter and do calculation

# IF answer is 1 (or -5 or -17),
#     THEN write step counter to setup
# ELSE
#     IF answer is in setup, 
#         THEN get steps from setup and add that to step counter, write number and steps to setup, 
#     ELSE continue calculation

if __name__ == "__main__":
    verbose = False
    
    # handle options and arguments passed to script
    try:
        myopts, args = getopt.getopt(sys.argv[1:],
                                     'vh',
                                     ['setup', 'verbose', 'help'])
    
    except getopt.GetoptError as e:
        onError(1, str(e))
    
    # if no options passed, then exit
    #if len(sys.argv) == 1:  # no options passed
    #    onError(2, 2)
    
    # interpret options and arguments
    for option, argument in myopts:
        if option in ('-v', '--verbose'):  # verbose output
            verbose = True
        elif option in ('-h', '--help'):  # display help text
            usage(0)

    # connect to database
    con = dbConnect(dbHost, dbName, dbUser, dbPass, verbose)
    curs = createCursor(con, verbose)
        
    # find lowest number not used
    number = findLowestNumber(curs, verbose)
    
    while True:
        # find lowest number not used
        number = findLowestNumber(curs, verbose)
        
        if number > 10000:
            break
        
        highestNumber, steps, numberList = collatz(curs, number, verbose)
        
        writeToDb(number, highestNumber, steps, "C", verbose)
    
        #if numberList:    
        #    numberList.pop(0)
    
        subSteps = steps
    
        if numberList:
            for numberAdd, highestNumber, steps in numberList:
                steps = subSteps -steps
                if verbose:
                    print("\n--- Adding numbers we got on the way ...")
                if verbose:
                    print("\n--- Number: " + str(numberAdd) + 
                          "\n    Highest: " + "0" + 
                          "\n    Steps: " + str(steps))
                writeToDb(numberAdd, 0, steps, "A", verbose)
                
        
                
                
        
    # disconnect from database
    closeCursor(curs, verbose)
    dbDisconnect(con, verbose)









