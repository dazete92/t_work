import sys
import os
import pprint
from collections import defaultdict
from netaddr import IPNetwork, IPAddress, IPRange

def defineGlobals():
   global prop_file_name
   prop_file_name = "vm.prop"

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
         ips[l.__str__()] = "root"

   return ips

def parseSessionData(sessions):

   session_db = defaultdict()

   for line in sessions.splitlines():
      chars = line.split(',')
      if chars[2] != 0:
         data = {'host': chars[0], 'success': chars[1], 'sessionNum': chars[2], \
         'user': chars[3], 'exploit': chars[4], 'type': chars[5], 'port': chars[6]}

         session_db[chars[0]] = data

   return session_db

def printRankingThresholds():
   
   print "Ranking Thresholds:"
   print "Excellent (6): Exploit will not crash the service."
   print "Great (5): Exploit auto-detects appropriate target operating system."
   print "Good (4): Exploit has a default target operating system."
   print "Normal (3): Exploit is reliable, but depends on specific OS."
   print "Average (2): Exploit is generally unreliable"