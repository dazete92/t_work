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
   
      i = "current" #raw_input("Enter command: ")
      command = i.split(' ')
      if command[0] == "current":
         break

      p = subprocess.Popen(['java', '-jar', 'cortana.jar', str(shared_util.prop_file_name), 'workspace.cna'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
      p.stdin.write("arguments %s %s" % (str(command[0]), str(command[1])))
      p.communicate()
      p.stdin.close()

   scan = raw_input("Perform scan on selected IPs? (y/n): ")
   return scan
   
def scan(ip_ranges, exclude, hosts):
   
   print "Initializing Nmap scan"
   ips = ""
   exs = ""
   args = 0;

   for i in range (0, len(ip_ranges)):
      ips += str(ip_ranges[i]) + ";"

   for i in range (0, len(exclude)):
      exs += str(exclude[i]) + ";"

   if ips is not "":
      args += 1
      print ips, exs
      ips = ips[:len(ips)-1]
      if exs is not "":
         exs = exs[:len(exs) - 1];
         args += 1
   
      p = subprocess.Popen(['java', '-jar', 'cortana.jar', str(shared_util.prop_file_name), 'nmap_scan.cna'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
   
      p.stdin.write("arguments %s %s %s" % (args, ips, exs))
      output = p.communicate()[0]

      print "Scan output: " + str(output)
      db = shared_util.parseIPRanges(output.splitlines())

      for host in hosts:
         if host in db:
            del db[host]

      return db

   return defaultdict()

def use_scanners(ip_ranges, hosts):

   print "Using Auxiliary Scanners"
   ips = ""

   for i in range (0, len(ip_ranges)):
      ips += str(ip_ranges[i]) + ";"

   if ips is not "":
      print ips
      ips = ips[:len(ips)-1] 

      print ips, hosts

      p = subprocess.Popen(['java', '-jar', 'cortana.jar', str(shared_util.prop_file_name), 'scanners.cna'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

      p.stdin.write("arguments %s" % ips)
      output = p.communicate()[0]

      print "Scanners output: " + str(output)
      db = shared_util.parseIPRanges(output.splitlines())

      for host in hosts:
         if host in db:
            del db[host]

      print db
      return db

   return defaultdict()