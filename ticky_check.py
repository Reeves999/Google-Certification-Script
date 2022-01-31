#!/usr/bin/env python3
import re
import sys
import subprocess
import csv
from operator import itemgetter

def State_count(Username, State, Info): # This Function finds the count or make one if need
    if Username not in Per_user['Info'] and Username not in Per_user['Error']:
        Per_user['Error'][Username] = 0
        Per_user['Info'][Username] = 0
        if State == 'INFO':
            Count = Per_user['Info'][Username] = 0
            return Count

        elif State == 'ERROR':
            if Info in Error.keys():
                Count = Error.get(Info,0)
                return Count

            else:
                Count = Error[Info] = 0
                return Count

        else:
            raise "The \'not\' is having a problem."

    elif Username in Per_user['Info'] and Username in Per_user['Error']:
        if State == 'INFO':
            Count = Per_user['Info'][Username]
            return Count

        elif State == 'ERROR':
            Count = Error.get(Info,0)
            return Count

        else:
            raise TypeError("Missing If condition!")

    else:
        raise ('\t Problem: is found---------- All if and elif statements passed!')

def Indexing_value(username,state,info,count): # This Function Add one everytime the Error or Info is listed
    try:
        if state == 'INFO':
            Per_user['Info'][username] = count + 1
            return
        elif state == 'ERROR':
            User_count = Per_user['Error'][username]
            Per_user['Error'][username] = User_count + 1
            Error[info] = count + 1
            return
        else:
            raise "Something slip thourgh the IF condition"

        return
    except:
        raise "Slip at beginning of Indexing_value"

def Csv_conversion(Per_user, Error): # This Function makes two csv files required for the html conversion and organizes the dict
    Headers = 'Username,INFO,ERROR'
    File_names = ['user_statistics.csv', 'error_message.csv']
    User = open(File_names[0], 'w')
    User.write(Headers)
    User.write('\n')
    Ram_list = []
    Counter = 0
    while Counter < len(Per_user["Info"].keys()):
        info_num =[str(num) for num in Per_user['Info'].values()]
        error_num = [str(num) for num in Per_user['Error'].values()]
        username = list(Per_user['Info'].keys())
        Ram_list.append("{},{},{}".format(username[Counter], info_num[Counter], error_num[Counter]))
        Counter += 1

    Ram_list = sorted(Ram_list)
    for sort in Ram_list:
        User.write(sort)
        User.write("\n")

    User.close()

    if Error:
        Headers = 'Error,Count'
        Error = dict(sorted(Error.items(), key = itemgetter(1), reverse=True))
        with open(File_names[1],'w') as Error_mesg:
            Error_mesg.write(Headers)
            Error_mesg.write('\n')

            Error_list = []
            Counter = 0
            while Counter < len(Error.keys()):

                Error_num = [str(num) for num in Error.values()]
                Info_name = list(Error.keys())
                Error_list.append("{},{}".format(Info_name[Counter], Error_num[Counter]))
                Counter += 1

            for sort in Error_list:
                Error_mesg.write(sort)
                Error_mesg.write("\n")

        return 'Done'

def Finisher_script(): # This function finishes the script by tying all the functions to gather
    global Per_user, Error, Filelog
    Per_user = {"Info":{}, "Error":{}} # Info:{Username:count} same for Error{}
    Error = {}
    Filelog = open("syslog.log","r")

    def Pattern(): # This function finds the required data in the log
        for log in Filelog:
            try:
                Info_pattern = re.compile(r"([INFO|ERROR]+) ([^\s].+) \[\S* \(([A-Za-z\.]*)")
                Full_pattern = Info_pattern.findall(log)
                if len(Full_pattern) == 0:
                    raise NoneType
                else:
                    (State,Info,Username) = Full_pattern[0]
                    yield Username, State, Info

            except:
                Error_pattern = re.compile(r"([INFO|ERROR]+) ([^\s].+) \(([A-Za-z\.]*)")
                Full_pattern = Error_pattern.findall(log)
                if len(Full_pattern) == 0:
                    raise NoneType
                else:
                    (State,Info,Username) = Full_pattern[0]
                    yield Username, State, Info

    for Username, State, Info in Pattern():
        Count = State_count(Username,State,Info)
        Indexing_value(Username,State,Info,Count)
    Csv_conversion(Per_user, Error)
    Filelog.close()
    return "Done with Script!!!!!"
Finisher_script()
