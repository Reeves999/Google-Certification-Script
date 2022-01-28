#!/usr/bin/env python3
import re
import sys
import subprocess
import csv

def State_count(State, Username, Info): # This Function finds the count or make one if need
    if Username not in Per_user['Info'] and State == 'INFO':
        Count = Per_user['Info'][Username] = 0
        return Count

    elif Username not in Per_user['Error'] and State == 'ERROR':
        Error_count = Error[Info]= 0
        User_count = Per_user['Error'][Username] = 0
        return Error_count, User_count

    elif Username in Per_user['Info'] and State == 'INFO':
        Count = Per_user['Info'][Username]
        return Count

    elif Username in Per_user['Error'] and State == 'ERROR':
        Error_count = Error['Info']
        User_count = User_per['Error'][Username]
        return Error_count, User_count

    else:
        return ('\t Problem: is found---------- All if and elif statements passed!')

def Indexing_value(username,state,info,count): # This Function Add one everytime the Error or Info is listed
    try:
        if state == 'INFO':
            Per_user['Info'][username] = count + 1
        elif state == 'ERROR':
            Per_user['Error'][username] = User_count + 1
            Error.update['Info'] = Error_count + 1
        return
    except SyntaxError:
        raise "FUckkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"

def Csv_conversion(Per_user, Error): # This Function makes two csv files required for the html conversion and organizes the dict
    File_names = ['user_statistics.csv', 'error_message.csv']
    if Per_user:
        Headers = ['Username', 'Info', 'Error']
        with open(File_names[0], 'w') as User:
            csvdict_object = csv.DictWriter(User, Headers)
            csvdict_object.writeheader()
            for key in Per_user:
                csvdict_object.writerow([key] + [Per user[key][counter] or for counter in counts])
            return
    else:
        Headers = ['Error Script', 'Number of Times Appear']
        with open(File_names[1],'w') as Error_mesg:
           csvdict_object = csv.DictWriter(Error_mesg, fieldnames=Headers)
           csvdict_object.writeheader()
           csvdict_object.writerow(Error)
           return

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
                if Info_pattern is None:
                    raise NoneType:
                else:
                    Full_pattern = Info_pattern.findall(log)
                    (State,Info,Username) = Full_pattern[0]
                    yield Username, State, Info
            except:
                Error_pattern = re.compile(r"([INFO|ERROR]+) ([^\s].+) \(([A-Za-z\.]*)")
                if Error_pattern is None:
                    raise NoneType
                else:
                    Full_pattern = Error_pattern.findall(log)
                    (State,Info,Username) = Full_pattern[0]
                    yield Username, State, Info

    for Username, State, Info in Pattern():
        Count = State_count(Username,State,Info)
        Indexing_value(Username,State,Info,Count)
        Csv_conversion(Per_user, Error)
    return Filelog.close()
Finisher_script()
