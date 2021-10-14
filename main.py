#!/usr/bin/python3
import getopt
from datetime import datetime, timedelta
import sys
import requests
import json


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def commandOptions(argv):
    opts, args = getopt.getopt(argv, "s:e:u:p:")
    options = {
        "start": "",
        "end": "",
        "user": "kfullerton",
        "pass": "",
       # "host": "http://192.168.11.190/zm/api/",
        "host": "http://krobx.dyndns.org:9002/zm/api/",
       # "host": "http://krherndon.dyndns.org:9001/zm/api/",
        "token": ""
    }
    if len(opts) < 4:
        print('main.py -s <start date> -d <end date> -u <user> -p <password>')
        print(' ALL OPTIONS are REQUIRED !!')
        sys.exit()

    for opt, arg in opts:
        if opt =="-s":
            options['start'] = arg
        elif opt == "-e":
            options['end'] = arg
        elif opt == "-u":
            options['user'] = arg
        elif opt == "-p":
            options['pass'] = arg


    return options

# "http://server/zm/api/events/index/StartTime%20>=:2015-05-15%2018:43:56/EndTime%20<=:208:43:56.json"
def getToken(options):
    # set the host url and send in the details.
    url = options['host'] + 'host/login.json?user=' + options['user'] + '&pass=' + options['pass']
    print("Attaching to " + options['host'])
    result = ""
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        result = data['access_token']
    else:
        print (r)
    return result

def deleteEvents(options):
    # use the start and end to get events
    # loop through then events and delete them

    # TODO: Get the start date and end date from command line

    events = {
        "total": 0,
        "archived": 0,
        "deleted": 0,
        "list": []
    }

    url = options['host'] + 'events.json?page=1&token=' + options['token']

    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        pg_count = data['pagination']['pageCount']
        for i in range(0, pg_count):
            print("Getting Page " + str(i), end = '\r' )
            if i % 5 == 0 and i != 0:
                print("")
            url = options['host'] + 'events.json?token=' + options['token'] + '&page=' + str(i)
            r = requests.get(url)
            if r.status_code == 200:
                d2 = r.json()
                for x in d2['events']:
                    evt = x['Event']                    
                    if(evt["Archived"] !="0"): #evt["Locked"] != false or 
                        events["archived"] +=1
                    else:
                        events['total'] +=1
                        events['list'].append(evt)
        print('-----------------------------------')
        print('-- Total Events:  ' + str(events["total"]))
        print('-- Archived:  ' + str(events["archived"]))
        print('-----------------------------------')
    x = 1
    for j in events['list']:
        x += 1
        durl = options['host'] + 'events/' + str(j["Id"]) + '.json?token=' + options['token']
        r3 = requests.delete(durl)
        if r3.status_code == 200:
            foo = str(x) + ' of ' + str(events["total"])
            print(foo + " Deleted  -  " + str(j["Id"]) + '  -  ' + str(j['StartTime']), end='\r' )
            if x % 10 == 0:
                print("")



# try
# except Exception as e:
#                         logging.info(str(e))





def main(argv):
    options = commandOptions(argv)
    if options['user'] != "" and options['pass'] != "":
        options['token'] = getToken(options)
        # print(token)
        if options['token'] != "":
            print('Logged In !')
            deleteEvents(options)
        else:
            print(' Did not log in')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
