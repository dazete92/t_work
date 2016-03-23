import sys
import time
import subprocess
import shared
from subprocess import Popen, PIPE, STDOUT
from collections import defaultdict

def parseData(chars):
   # chars format =  host IP address, port, protocol, name, state (open/closed), info

   return (chars[0], chars[1], chars[2], chars[3], chars[4], chars[5])
      
def print_db(db):
   # prints services database contents
   
   for key in db:
      print key, len(db[key])
      for i in range(len(db[key])):
         print db[key][i]
         
def write_db_to_file(output):
   db_file = open("db_services.txt", 'w')
   
   for line in output.splitlines():
      chars = line.split(',')
      (host, port, protocol, name, state, info) = parseData(chars)
         
      # writes exploit data to file
      
      dataString = str(host) + "," + str(port) + "," + str(protocol) + "," + \
         str(name) + "," + str(state) + "," + str(info)
   
      db_file.write(dataString)
      db_file.write("\n")
   
      db_file.close()

def generate_db():

   print "Generating service database"
   db = defaultdict()

   p = subprocess.Popen(['java', '-jar', 'cortana.jar', str(shared.prop_file_name), 'services.cna'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
       
   output = p.communicate()[0]
   
   for line in output.splitlines():
      chars = line.split(',')
      (host, port, protocol, name, state, info) = parseData(chars)

      # creates dictionary of information for each exploit
      data = {'port': port, 'protocol': protocol, 'name': name, 'state': state,
         'info': info}
      
      # creates a searchable database of exploits, organized by port number
      if host not in db:
         db[host] = []
      db[host].append(data)
         
   return db
   
