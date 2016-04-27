import sys
import time
import subprocess
import shared_util
from operator import itemgetter
from subprocess import Popen, PIPE, STDOUT
from collections import defaultdict

def print_attacks(attacks):
   
   for host in attacks:
      print host
      for attack in range(len(attacks[host])):
         print attacks[host][attack]

           
def determineAttackVectors(db_e, db_s, db_h, host_list, severity):
   # figures out attack vectors based on hosts and services
   print "Creating Attack Vectors"

   db = defaultdict()
   
   for host in db_h:
      if host in host_list:
         db[host] = []
         services_list = db_s[host]
         for service in services_list:
            if service['state'] == "open" or service['state'] == "unknown":
               if service['port'] in db_e:
                  for exploit in range(len(db_e[service['port']])):
                     if db_e[service['port']][exploit]['modRank'] >= severity:
                        if db_e[service['port']][exploit]['os'] == db_h[host]['os_name']:
                           db[host].append(db_e[service['port']][exploit])
                        if db_h[host]['os_name'] == "linux" and db_e[service['port']][exploit]['os'] == "unix":
                           db[host].append(db_e[service['port']][exploit])
                        if db_e[service['port']][exploit]['os'] == "multi":
                           db[host].append(db_e[service['port']][exploit])
   
   #for host in host_list:
      #db[host] = sorted(db[host], key=itemgetter('modRank'), reverse=True)
             
   return db

def generate_attacks(attacks, server_ip, severity):
   
   print "Generating attack string"

   lhost = server_ip
   string = ""
   counter = 0
   output = ""

   for host in attacks:
      rhost = host
      for attack in range(len(attacks[host])):
         name = attacks[host][attack]['name']
         rank = attacks[host][attack]['modRank']
         string += str(rhost) + "," + str(name) + "," + str(lhost) + "," + str(rank) + ";"
         counter += 1

   if string is not "":
      print "Launching attack string"    
      p = subprocess.Popen(['java', '-jar', 'cortana.jar', str(shared_util.prop_file_name), 'attacks.cna'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)   
      p.stdin.write("arguments %s %s %s" % (str(counter), string, severity))
      output = p.communicate()[0]
      p.stdin.close();
      print output
      
   return getSessionsAndExploits(output)

def getSessionsAndExploits(output):

   session_db = defaultdict()
   exploitsRun = defaultdict()
   i = 0

   lines = output.splitlines()
   print "Lines: " + str(len(lines))
   while i < len(lines):
      print lines[i]
      chars = lines[i].split(',')
      if chars[2] != 0:
         data = {'host': chars[0], 'success': chars[1], 'sessionNum': chars[2], \
         'user': chars[3], 'exploit': chars[4], 'type': chars[5], 'port': chars[6], \
         'numRun': chars[7]}

         session_db[chars[0]] = data

      host = chars[0]
      exploits_run = chars[7]
      j = 0
      print "exploits run: " + str(exploits_run)
      while j < int(exploits_run):
         print i + (j + 1), i, j
         chars = lines[i + (j + 1)].split(',')
         data = {'name': chars[0], 'success': chars[1]}

         if host not in exploitsRun:
            exploitsRun[host] = []
         exploitsRun[host].append(data)
         j += 1
      i += j + 1

   print session_db, exploitsRun
   return (session_db, exploitsRun)

'''
send attacks unordered
for each host, store attacks in bins based on modrank
generate percentages based on number of bins
randomly select bin, randomly select exploit from bin
run exploit, remove from bin, store in array
preface: host,flag,sessionNum,user,type,# of exploits launched
         exploit_name, 0 for fail, 1 for success
'''