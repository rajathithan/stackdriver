# Author : Rajathithan Rajasekar
# Google cloud script for retreiving stackdriver logs in local windows desktop
# multiprocessing enabled



import os, sys, time, subprocess
import multiprocessing
from multiprocessing import Pool
import pprint
import re
import json
from dateutil.parser import parse
from datetime import datetime as dt
from datetime import timedelta
import ast
from tqdm import tqdm



def build_query(): 
    result = []
    completedquery = 0
    while True:
        if completedquery == 1:
            return startdate, enddate ,''.join(result) 
            break
        else:
            selection = input("Press any key to enter or q to  exit:\n")
            if selection == "q" or selection == "Q":
                break
                return 0,0,0
            else:
                print("Enter the date and time to filter the results:")
                startdate = input("Enter start date in 'yyyy-mm-dd hh:mm:ss' format:\n")    
                #startdate = "2020-05-12 01:00:00"           
                checkdt(startdate)
                enddate = input("\nEnter end date in 'yyyy-mm-dd hh:mm:ss' format:\n")
                #enddate = "2020-05-12 01:00:20" 
                checkdt(enddate)          
                while True:
                    fieldpath = input("\nEnter the field name path details: (e.g resource.type)\n")  
                    #fieldpath = "resource.type"             
                    fieldvalue = input("\nEnter the field value details: ( e.g http_load_balancer )\n")
                    #fieldvalue = "http_load_balancer"
                    result.append(fieldpath + " = " + fieldvalue)
                    fieldselection = input("\nPress any key to add fields or press q exit adding fields:\n")                
                    if fieldselection == "q" or fieldselection == "Q":
                        completedquery = 1
                        break                        
                    else:
                        boolop= input("\nEnter the boolean operator: ( e.g AND | OR ):\n")    
                        result.append(" "+ boolop +" ")

     
def checkdt(stetdate):
    try: 
        dt.strptime(stetdate, "%Y-%m-%d %H:%M:%S")        
    except ValueError:
        print("\nPlease enter date and time in proper format !!!\n")
        print("Exiting the program...")
        sys.exit()


def seconddifference(st,et):
    st = dt.strptime(st, "%Y-%m-%d %H:%M:%S")
    et = dt.strptime(et, "%Y-%m-%d %H:%M:%S")
    mdiff = et -st
    return st, et, round(mdiff.total_seconds())



def mpro(st,tsec,query):
    stime = time.time()
    p = Pool()
    global pctst1, pctst2
    loginput = []
    tsec = tsec + 1
    #print(tsec)
    tseconds = range(tsec)
    tseconds = tseconds[1:]    
    for i in tseconds:
        loginput.append((i,st,query))
    #print(loginput)    
    result = p.starmap(getLogs,loginput)
    etime = time.time() 
    regex = re.compile(r'[\n\r]')
    finalresult = ",".join(result)
    finalresult = regex.sub("", finalresult)
    res = ast.literal_eval(finalresult)
    tuplen = len(res) 
    filename = input("Enter the filename to save the data in *.log format:\n")
    if os.path.exists(filename+'.log'):
        logFile = open(filename +'.log', 'w')
        logFile.close()
    else:
        logFile = open(filename +'.log', 'x')
        logFile.close() 
    for n in range(tuplen):
        #print(n)
        res1 = json.loads(json.dumps(res[n]))
        res1.reverse()
        logFile = open(filename +'.log', 'a')
        pp = pprint.PrettyPrinter(indent=4, stream=logFile)                     
        for item in res1:
            pp.pprint(item)
        logFile.close()
    
    ttime = etime - stime   
    print("\n**************************************************************\n")
    print(f'Total time taken by the program for extraction is - {round(ttime)} - secs \n')
    print("**************************************************************\n")
    print(f"Extracted logs are saved in {filename}.log")

def getLogs(sec,st,query):
    try:
        with tqdm(unit='B', unit_scale=True, miniters=1, desc="getLogs={}".format(sec,st,query)) as t:
            starttime = time.time()
            pctst2 = st    
            pctst2 = str(pctst2)    
            pctst2 = dt.strptime(pctst2, "%Y-%m-%d %H:%M:%S")      
            pctst2 =  pctst2 + timedelta(seconds=sec)
                
            pctst1 = pctst2 - timedelta(seconds=1)
            pctst1 = str(pctst1)
            pctst1 = dt.strptime(pctst1, "%Y-%m-%d %H:%M:%S")

            fctst1 =  dt.strftime(pctst1, "%Y-%m-%dT%H:%M:%SZ")
            fctst2 =  dt.strftime(pctst2, "%Y-%m-%dT%H:%M:%SZ")

            if sec == 1:
                truequery = 'gcloud logging read "timestamp^>=""'+ fctst1 + '"" AND timestamp^<=""'+ fctst2 + '"" AND ' + query + '" --format json'
            else:
                truequery = 'gcloud logging read "timestamp^>""'+ fctst1 + '"" AND timestamp^<=""'+ fctst2 + '"" AND ' + query + '" --format json'
            sbp = subprocess.Popen(truequery, shell=True, stdout = subprocess.PIPE)
            stdout, stderr = sbp.communicate()
            for line in stdout:
                t.update()                
            endtime = time.time()
            totaltime = endtime - starttime
            #print(f'\nTotal time taken by process No: {sec} - PID : {os.getpid()} - is - {round(totaltime)} secs \n')
            return stdout.decode("utf-8")
    except:
        pass
    


def checkgcloud():
    print("Checking for gcloud installation")
    if os.path.exists("validation.log"):
        pass
    else:
        logoutput = open("validation.log","w")
        logoutput.close()
    filepath= ["gcloud version"]     
    params2 = [">",
                "validation.log"]
    p = subprocess.Popen([filepath] + params2, shell=True, stdout = subprocess.PIPE)
    stdout, stderr = p.communicate() 
    logoutput = open("validation.log","r")
    for line in logoutput:
        if 'Google Cloud SDK' in line:
            break
        else:
            print("No Google cloud SDK found")
            sys.exit()
    logoutput.close()
    

def getcurrentAccount():
    print("\nGetting current account")
    if os.path.exists("currentaccount.log"):
        pass
    else:
        logoutput = open("currentaccount.log","w")
        logoutput.close()
    filepath= ["gcloud auth list --filter=status:ACTIVE --format=value(ACCOUNT)"]     
    params2 = [">",
                "currentaccount.log"]
    p = subprocess.Popen([filepath] + params2, shell=True, stdout = subprocess.PIPE)
    stdout, stderr = p.communicate() 
    logoutput = open("currentaccount.log","r")
    for line in logoutput:
        print("\n================================================")
        print("Current Account:")
        print("================================================")
        print(line)
    logoutput.close()


def getcurrentProject():
    print("\nGetting current Project")
    if os.path.exists("currentproject.log"):
        pass
    else:
        logoutput = open("currentproject.log","w")
        logoutput.close()
    filepath= ["gcloud config list --format=value(core.project)"]     
    params2 = [">",
                "currentproject.log"]
    p = subprocess.Popen([filepath] + params2, shell=True, stdout = subprocess.PIPE)
    stdout, stderr = p.communicate() 
    logoutput = open("currentproject.log","r")
    for line in logoutput:
        print("\n================================================")
        print("Current Project:")
        print("================================================")
        print(line)
    logoutput.close()



if __name__ == '__main__':   
    multiprocessing.freeze_support()
    checkgcloud()
    getcurrentAccount()
    getcurrentProject()
    print("\n================================================")
    print("Filter and Download the GCP logs of your choice:")
    print("================================================")
    print("\n")
    print("Let's build the query,")
    st, et, query = build_query()
    st, et, tsec = seconddifference(st,et)
    print(f"you have entered the start date and  time as: \n{st}")
    print(f"you have entered the end date and time as: \n{et}")
    print(f"Total processes required to complete the extract: \n{tsec}")
    print(f"you have entered the query as: \n{query}")
    print("\nMulti processing the query now:\n")
    mpro(st,tsec,query)

   