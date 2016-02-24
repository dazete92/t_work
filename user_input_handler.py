import sys
import os
from netaddr import IPNetwork, IPAddress
import pprint

def print_header():
   print "Adaptive Exploitation and Targeted Pentesting System"
   print ""

def prompt_user():

   ip_ranges = []
   target_ip = ""
   target_path = ""
   server_ip = ""
   server_passwd = ""

   print "\nPlease provide credentials to start or connect to an existing teamserver"
   server_params = raw_input("<host IP> <server password>: ")
   server_list = server_params.split(' ')
   server_ip = server_list[0]
   server_passwd = server_list[1]

   print "\nPlease provide the IP ranges of the machines to be scanned in CIDR format: "
   input_params = raw_input("<ipRange1> <ipRange2> ...: ") 
   input_list = input_params.split(' ')
   for i in range (0, len(input_list)):
      ip_ranges.append(input_list[i])
      
   target_ip = raw_input("\nIf desired, select a target machine: <target IP>: ")
   target_location = isTargetInRange(ip_ranges, target_ip) if target_ip != "" else False

   #severity = raw_input("Enter an exploitation reliability threshold (1 - 5, 1 = poor, 5 = excellent): ")
   severity = 6
      
   return (server_ip, server_passwd, ip_ranges, target_ip, target_location, severity)
   
def isTargetInRange(ip_ranges, target_ip):

   target = int(IPAddress(target_ip))

   for i in range(0, len(ip_ranges)):
      ip = IPNetwork(ip_ranges[i])
      if (ip.first <= target and ip.last >= target):
         return True

   return False
