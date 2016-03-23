import sys
import os
from netaddr import IPNetwork, IPAddress, IPRange
import pprint
import shared
from collections import defaultdict

def print_header():
   print "Adaptive Exploitation and Targeted Pentesting System"
   print ""

def prompt_user(prop_file_gen):

   ip_ranges = []
   target_ip = ""
   target_path = ""
   server_ip = ""
   server_passwd = ""

   #print "\nPlease provide credentials to start or connect to an existing teamserver"
   #server_params = raw_input("<host IP> <server password>: ")
   #server_list = server_params.split(' ')
   server_ip = "172.16.221.1" #server_list[0]
   server_passwd = "pass" #server_list[1]

   #print "\nPlease provide the IP ranges of the machines to be scanned in CIDR format: "
   #input_params = raw_input("<ipRange1> <ipRange2> ...: ") 
   input_list = "172.16.221.132/31".split(' ') #input_params.split(' ')
   for i in range (0, len(input_list)):
      ip_ranges.append(input_list[i])

   host_list = parseIPRanges(ip_ranges)
      
   target_ip = "" #raw_input("\nIf desired, select a target machine: <target IP>: ")
   target_location = False #isTargetInRange(ip_ranges, target_ip) if target_ip != "" else False

   #severity = raw_input("Enter an exploitation reliability threshold (1 - 5, 1 = poor, 5 = excellent): ")
   severity = 6

   prop_file = ""
   if prop_file_gen is True:
      #shared.prop_file_name = raw_input("\nPlease provide the name of the .prop file to be used to connect to the team server: ")

   return (server_ip, server_passwd, ip_ranges, target_ip, target_location, severity)
   
def isTargetInRange(ip_ranges, target_ip):

   target = int(IPAddress(target_ip))

   for i in range(0, len(ip_ranges)):
      ip = IPNetwork(ip_ranges[i])
      if (ip.first <= target and ip.last >= target):
         return True

   return False

def parseIPRanges(ip_ranges):

   ips = defaultdict()

   for i in range(0, len(ip_ranges)):
      ip = IPNetwork(ip_ranges[i])
      for l in list(ip):
         ips[l.__str__()] = []

   return ips
         
      