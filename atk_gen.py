import sys
import time
import subprocess
import shared_util
from operator import itemgetter
from subprocess import Popen, PIPE, STDOUT
from collections import defaultdict

def print_attacks(attacks):
   
   for host in attacks:
      for attack in range(len(attacks[host])):
         print attacks[host][attack]['name'], attacks[host][attack]['modRank']

           
def determineAttackVectors(db_e, db_s, db_h, host_list):
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
                     if db_e[service['port']][exploit]['os'] == db_h[host]['os_name']:
                        db[host].append(db_e[service['port']][exploit])
                     if db_h[host]['os_name'] == "linux" and db_e[service['port']][exploit]['os'] == "unix":
                        db[host].append(db_e[service['port']][exploit])
                     if db_e[service['port']][exploit]['os'] == "multi":
                        db[host].append(db_e[service['port']][exploit])
   
   for host in host_list:
      db[host] = sorted(db[host], key=itemgetter('rankNum'), reverse=True)
             
   return db

def generate_attacks(attacks, db_h):
   
   print "Generating attack string"

   lhost = "172.16.222.1"
   string = ""
   counter = 0
   p = subprocess.Popen(['java', '-jar', 'cortana.jar', str(shared_util.prop_file_name), 'attacks_copy.cna'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
   for host in attacks:
      rhost = host
      for attack in range(len(attacks[host])):
         name = attacks[host][attack]['name']
	      string += str(rhost) + "," + str(name) + "," + str(lhost) + ";"
	      counter += 1

   print "Launching attack string"         
   p.stdin.write("arguments %s %s" % (str(counter), string))
   output = p.communicate()[0]
   p.stdin.close();
   
   return output
      