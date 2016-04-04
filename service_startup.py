import sys
import time
import subprocess
import shared_util

def init(ip, passwd):

   print "Starting Postgresql..."
   p = subprocess.Popen(['sudo', 'service', 'postgresql', 'start'])

   print "Initializing the Cortana team server..."
   p = subprocess.Popen(['sudo', 'teamserver', str(ip), str(passwd)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

   print "Sleeping for 45 seconds..."
   time.sleep(45)

   print "Creating .prop file..."
   prop_file = open(shared_util.prop_file_name, "w")
   prop_file.write("host=" + str(ip) + "\n")
   prop_file.write("port=55553\n")
   prop_file.write("user=cortana\n")
   prop_file.write("passwd=" + str(passwd) + "\n")
   prop_file.close()

   print "Created " + str(shared_util.prop_file_name)
   
def update():
   print "Updating Metasploit..."
   p = subprocess.Popen(['sudo', 'msfupdate'])
   output = p.communicate()
