import sys
import os
import shared_util
from collections import defaultdict

def print_header():
   print "Adaptive Exploitation and Targeted Pentesting System"
   print ""

def prompt_user(prop_file_gen):

   ip_ranges = []
   target_ip = ""
   server_ip = ""
   server_passwd = ""

   #print "\nPlease provide credentials to start or connect to an existing teamserver"
   #server_params = raw_input("<host IP> <server password>: ")
   #server_list = server_params.split(' ')
   server_ip = "172.16.221.1" #server_list[0]
   server_passwd = "pass" #server_list[1]

   #print "\nPlease provide the IP ranges of the machines to be scanned in CIDR format: "
   #input_params = raw_input("<ipRange1> <ipRange2> ...: ") 
   input_list = "172.16.221.132 172.16.221.136 172.16.221.128".split(' ') #input_params.split(' ')
   for i in range (0, len(input_list)):
      ip_ranges.append(input_list[i])
      
   target_ip = "172.16.221.136" #raw_input("\nIf desired, select a target machine: <target IP>: ")

   #shared_util.printRankingThresholds()
   #severity = raw_input("Enter an exploit ranking threshold (default = 4): ")
   #if (severity == ""):
      #severity = 4
   severity = 5
   '''
   add severity metrics from wiki page
   '''

   return (server_ip, server_passwd, ip_ranges, target_ip, severity)