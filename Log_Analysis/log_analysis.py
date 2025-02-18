import os
import os.path
import json
import subprocess
import pprint

def getUserAuthTimes(username):
   """
   Returns a list of the dates of login for user userid from log/auth.log
   """
   with open("./log/auth.log.all", "r") as f:
       lines = f.readlines()
       date_time_line = []
       for line in lines:
           if username in line and "Accepted" in line:
               bits = line.split()
               date_time = " ".join(bits[:3])
               date_time_line.append(date_time)
       return list(set(date_time_line))

def getInvalidLogins():
   """
   Returns a dictionary mapping invalid user ids to # of failed logins on log/auth.log
   """
   with open("./log/auth.log.all", "r") as f:
       lines = f.readlines()
       denied_users = {}
       for line in lines:
           if "Invalid user" in line:
               user = line.split("Invalid user ")[1].split(" ")[0]
               if user in denied_users:
                   denied_users[user] += 1
               else:
                   denied_users[user] = 1
       return denied_users

def extractLogFiles(logfile, logdir="./log"):
   """
   Extract all gzipped files for a specified file. Put them in a combined file.
   """
   logfiles = []
   for file in os.listdir(logdir):
       if logfile in file and file.endswith(".gz"):
           logfiles.append(os.path.join(logdir, file))
  
   with open(logfile + ".all", "wb") as outfile:
       for file in logfiles:
           with open(file, "rb") as infile:
               outfile.write(infile.read())
   return True

def compareInvalidIPs():
    """
    Find all IP addresses for invalid logins, then see which IPs are also used for scanning
    """
    denied_ips = set()
    with open("./log/auth.log.all", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "Invalid" in line:
                ip = line.split(" from ")[1].split(" ")[0].strip()
                denied_ips.add(ip)
    # print(denied_ips)
    ip_scan = set()
    with open("./log/ufw.log.all", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "BLOCK" in line:
                ip = line.split("SRC=")[1].split(" ")[0]
                ip_scan.add(ip)
    # print(ip_scan)
    mutual_ips = denied_ips.intersection(ip_scan)
    return mutual_ips
   

if __name__ == "__main__":
   print(getUserAuthTimes("tmoore"))
   print(getInvalidLogins())
   extractLogFiles("auth.log.all")
   extractLogFiles("ufw.log.all")
   print(compareInvalidIPs())
   
 


