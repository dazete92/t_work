import sys
import os
import pprint
import shared_util
from collections import defaultdict
from netaddr import IPNetwork, IPAddress, IPRange

def defineGlobals():
   global prop_file_name
   prop_file_name = ".connect.prop"

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
         ips[l.__str__()] = ""

   return ips

def getCIDR(addr, mask):

   ip = IPNetwork(str(addr) + "/" + str(mask))
   return ip.__str__()

def parseSessionData(sessions):

   session_db = defaultdict()

   for line in sessions.splitlines():
      chars = line.split(',')    #host, success?, sessionNum, user, exploit
      data = {'host': chars[0], 'success': chars[1], 'sessionNum': chars[2], \
        'user': chars[3], 'exploit': chars[4], 'type': chars[5]}

      session_db[chars[0]] = data

   return session_db