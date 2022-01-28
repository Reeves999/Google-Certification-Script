#!/usr/bin/env python3
import re
import sys
import subprocess
import csv

def State_count(Username, State, Info): # This Function finds the count or make one if need
    if Username not in Per_user['Info'] and State == 'INFO':
        Count = Per_user['Info'][Username] = 0
        return Count

    elif Username not in Per_user['Error'] and State == 'ERROR':
        User_count = Per_user['Error'][Username] = 0
        Count = Error[Info] = 0
        return Count
        if Per_user['Info'].get(Username) == None:
            Per_user['Info'][Username] = 0
            return Count
        else:
            return Count

    elif Username in Per_user['Info'] and State == 'INFO':
        Count = Per_user['Info'][Username]
        if Per_user['Error'].get(Username) == None:
            Per_user['Error'][Username] = 0
            return Count
        else:
            return Count


    elif Username in Per_user['Error'] and State == 'ERROR':
        Count = Error.get(Info)
        if Count == None:
            Count = Error[Info] = 0
            return Count
        else:
            return Count

    else:
        raise ('\t Problem: is found---------- All if and elif statements passed!')

def Indexing_value(username,state,info,count): # This Function Add one everytime the Error or Info is listed
    try:
        if state == 'INFO':
            Per_user['Info'][username] = count + 1
            return
        elif state == 'ERROR':
            User_count = Per_user['Error'][username]
            if User_count != None:
                Per_user['Error'][username] = User_count + 1
                Error[info] = count + 1
            return
    except:
        raise "FUckkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"

def Csv_conversion(Per_user, Error): # This Function makes two csv files required for the html conversion and organizes the dict

    def Inter_loop(Per_user):
        Ram_list = []
        Per_user_list = []
        for name, values in Per_user.items():
            if isinstance(values, dict):
                Inter_loop(values)
            else:
                Per_user_list += (name, values)
                if  len(Ram_list) == 0:
                    Ram_list.append(values)
                    Ram_list.append(name)
                elif len(Ram_list) == 2:
                    Ram_list.append(values)
                elif len(Ram_list) == 3:
                    print(Ram_list[0])
                    print(('{}, {}, {} \n'.format(Ram_list[0], Ram_list[1], Ram_list[2])))
                    Per_user_list.append('{}, {}, {} \n'.format(Ram_list[0], Ram_list[1], Ram_list[2]))
                    Ram_list.clear()
                else:
                    raise "_____________Bug__________---"
            return print(Per_user_list)


    Headers = 'Username, INFO, ERROR'
    File_names = ['user_statistics.csv', 'error_message.csv']
    User = open(File_names[0], 'w')
    User.write(Headers)
    User.write('\n')
    sam = Inter_loop(Per_user)
    # print(Per_user_list)
    print(sam)
        # Sort = sorted(row)
        # User.write(Sort)



    User.close()

        #print(list_username,list_len_info,list_len_error)
        #for x in range(1):# goes through one item of the list
        #    count = 0
        #    Frame = []
            #for row in list_len_error:# goes through whole list
                #username, error_num = row
                #error_str = str(error_num)
                #info_str = str(list_len_info[len])
                #username_str = str(username)
                #if username_str < list_len_error[count]:
                #Frame.append("{}, {}, {} \n".format(username.lower(),info_str,error_str))
                #count += 1

    #Sort_frame = (sorted(tuple(Frame)))
    #for row in Sort_frame:
    #    User.write(row)
                #Sort_frame = sorted(Frame)
                #print(Sort_frame)
                #for x in Sort_frame:
                #User.write(x)

    if Error:
        Headers = 'Error, Count'
        Error = dict(sorted(Error.items(), key=lambda count: count[1], reverse=True))
        with open(File_names[1],'w') as Error_mesg:
            Error_mesg.write(Headers)
            Error_mesg.write('\n')
            for key,error in Error.items():
                row_string = '{}, {}'.format(key,error)
                Error_mesg.write(row_string)
                Error_mesg.write('\n')

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
                #print(Full_pattern)
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
