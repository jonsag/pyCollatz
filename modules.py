#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys, configparser, os


config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# read variables from config file
dbHost = config.get('db', 'dbhost').strip()
dbName = config.get('db', 'dbname').strip()
dbUser = config.get('db', 'dbuser').strip()
dbPass = config.get('db', 'dbpass').strip()

# handle errors
def onError(errorCode, extra):
    print("\nError:")
    if errorCode == 1: # print error information, print usage and exit
        print(extra)
        usage(errorCode)
    elif errorCode == 2: # no argument given to option, print usage and exit
        print("No options given")
        usage(errorCode)
    elif errorCode in (3, 4, 5, 6, 7): # print error information and exit
        print(extra)
        sys.exit(errorCode)
    elif errorCode in(6, 7): # print error information and return running program
        print(extra)
        return
        
# print usage information        
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s <options>" % sys.argv[0])
    print("\nOptions: ")
    print("  -c, --connect")
    print("    Connect to remote host")
    print("  -a, --add")
    print("    Add hosts, usernames etc.")
    print("  -e, --edit")
    print("    Edit hosts, usernames etc.")
    print("  -p, --print")
    print("    Prints all hosts, usernames etc. on screen")
    print("  -s, --show")
    print("    Shows passwords in plain text")
    print("  -v, --verbose")
    print("    Verbose output")
    print("  -h, --help")
    print("    Prints this")
    sys.exit(exitCode)
             
