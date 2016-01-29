import sys
import os

def print_header():
   print "Adaptive Exploitation and Targeted Pentesting System"
   print ""

def prompt_user():

   ip_ranges = []
   target_ip = ""
   target_path = ""
   server_ip = ""
   server_passwd = ""

   server_params = raw_input("Please provide the following: <host IP> <server password>: ")
   server_list = server_params.split(' ')
   server_ip = server_list[0]
   server_passwd = server_list[1]

   input_params = raw_input("# of IP ranges ipRange1 ipRange2 etc.: ") 
   input_list = input_params.split(' ')
   for i in range (1, len(input_list)):
      ip_ranges.append(input_list[i])
      
   target_params = raw_input("If desired, select a target: <target IP> <path to target>: ")
   target_list = target_params.split(' ')
   
   if len(target_list) >= 1:
      target_ip = target_list[0]
   if len(target_list) == 2:
      target_path = target_list[1]

   severity = raw_input("Enter an exploitation reliability threshold (1 - 5, 1 = poor, 5 = excellent): ")
      
   return (server_ip, server_passwd, ip_ranges, target_ip, target_path, severity)
   
   
