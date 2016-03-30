import sys
import subprocess
import shared_util
from collections import defaultdict

def scan_location_setup():

   command = ""

   print "\nDetermine destination of scan data or previous scan data\n"
   
   print "Prop file name: " + str(shared_util.prop_file_name)

   while True:
      print "Workspaces (* = current):"
      p = subprocess.Popen(['java', '-jar', 'cortana.jar', str(shared_util.prop_file_name), 'workspace.cna'], stdin=subprocess.PIPE)
      p.stdin.write("arguments %s" % "list")
      p.communicate()
      p.stdin.close()
   
      print "Commands:"
      print " > add <workspace name>      Add a workspace"
      print " > delete <workspace name>   Delete a workspace"
      print " > switch <workspace name>   Switch to an existing workspace"
      print " > current                   Use current settings\n"
   
      i = raw_input("Enter command: ")
      command = i.split(' ')
      if command[0] == "current":
         break

      p = subprocess.Popen(['java', '-jar', 'cortana.jar', str(shared_util.prop_file_name), 'workspace.cna'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
      p.stdin.write("arguments %s %s" % (str(command[0]), str(command[1])))
      p.communicate()
      p.stdin.close()

   scan = raw_input("Perform scan on selected IPs? (y/n): ")
   return scan
   
def scan(ip_ranges):
   
   print "Initializing Nmap scan"
   ips = ""
   
   p = subprocess.Popen(['java', '-jar', 'cortana.jar', str(shared_util.prop_file_name), 'nmap_scan.cna'], stdout=subprocess.PIPE, stdin=subprocess.PIPE);
   
   for i in range (0, len(ip_ranges)):
      ips += str(ip_ranges[i]) + ";"  
   ips = ips[:len(ips)-1]
   
   p.stdin.write("arguments %s" % ips)
   output = p.communicate()[0]
   
   return shared_util.parseIPRanges(output.splitlines())