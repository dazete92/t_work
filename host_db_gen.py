import sys
import time
import subprocess
from subprocess import Popen, PIPE, STDOUT
from collections import defaultdict

def parseData(chars):
   # chars format = host IP address, MAC address, host name, os name, os flavor, os version, host type, info, comments

   os_name = chars[1].split(' ')

   return (chars[0], os_name[0].lower())
      
def print_db(db):
   # prints hosts database contents
   
   for key in db:
      print key, db[key]
         
def write_db_to_file(output):
   db_file = open("db_hosts.txt", 'w')
   
   for line in output.splitlines():
      chars = line.split(',')
      (ip, mac, name, os_name, os_flav, os_v, host_type, info, comments) = parseData(chars)
         
      # writes host data to file
      
      dataString = str(ip) + "," + str(mac) + "," + str(name) + "," + str(os_name) + \
      "," + str(os_flav) + "," + str(os_v) + "," + str(host_type) + "," + str(info) \
      + "," + str(comments)
   
      db_file.write(dataString)
      db_file.write("\n")
   
      db_file.close()

def generate_db():

   db = defaultdict()

   p = subprocess.Popen(['java', '-jar', 'cortana.jar', 'vm.prop', 'hosts.cna'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
       
   output = p.communicate()[0]
   
   for line in output.splitlines():
      chars = line.split(',')
      #print chars
      (ip, os_name) = parseData(chars)

      # creates dictionary of information for each host
      data = {'ip': ip, 'os_name': os_name}
      
      # creates a searchable database of hosts, organized by ip address
      if ip not in db:
         db[ip] = data
         
   return db
   
