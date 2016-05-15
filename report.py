import shared_util
from collections import defaultdict

def generateReport(ip_ranges, host_list, db_h, sessions, hierarchy, 
   alteredSessions, targetTree, user_ranges, target_ip, severity, db_e, db_s, attacks_final):

   printUserInformation(user_ranges, target_ip, severity)
   comp_hosts = printDiscoveredMachines(db_h, sessions, alteredSessions, db_e, hierarchy, db_s, attacks_final)
   if target_ip is not "":
      if target_ip in sessions and sessions[target_ip]['success'] == "true":
         print "TARGET WAS COMPROMISED:"
      else:
         print "TARGET WAS EITHER NOT COMPROMISED OR NOT FOUND"
      printTree(targetTree, target_ip, comp_hosts)
   else:
      print "TARGET WAS NOT SPECIFIED"

def printTree(tree, target_ip, comp_hosts):

   counter = 0
   parents = []
   children = []

   print "Target: " + str(target_ip)
   parents.append(target_ip)
   del tree[target_ip]
   comp_hosts["root"] = {'compromised': False}

   while len(tree) > 0:
      counter += 1
      print determineOrdinalNumber(counter) + " connections:"
      for parent in parents:
         for node in tree:
            if tree[node] == parent:
               p_string = parent if comp_hosts[parent]['compromised'] == False else str(parent + "(C)")
               c_string = node if comp_hosts[node]['compromised'] == False else str(node + "(C)")
               print "parent: " + str(p_string) + " -> child: " + str(c_string)
               children.append(node)

      for child in children:
         del tree[child]

      parents = children
      children = []

def printUserInformation(user_ranges, target_ip, severity):

   target = ""
   print "-----Provided IP Address and/or ranges-----"
   for i in range (0, len(user_ranges)):
      print user_ranges[i]

   if target_ip is "":
      target = "None"
   else:
      target = target_ip
   print "Target IP Address: " + str(target)
   print "Exploit Ranking Threshold: " + str(severity) + " (" + str(getSeverity(str(severity))) + ")"

def printDiscoveredMachines(db_h, sessions, alteredSessions, db_e, hierarchy, db_s, attacks):

   comp_hosts = defaultdict()

   print "-----Discovered Machines-------------------"
   for h in db_h:
      host = db_h[h]
      print "HOST: " + host['ip']
      compromised = True if sessions[host['ip']]['success'] == "true" else False
      print "  OS: " + host['os_name']
      print "  VERSION: " + host['os_version']
      print "  EXPLOITS GENERATED: " + str(len(attacks[host['ip']]))
      print "  EXPLOITS ATTEMPTED: " + sessions[host['ip']]['numRun']
      print "  COMPROMISED: Yes" if compromised == True else "  COMPROMISED: No"
      comp_hosts[host['ip']] = {'compromised': compromised}
      if compromised == True:
         exploit = findExploit(host['ip'], sessions, db_e)
         print "  EXPLOIT:"
         print "     NAME: " + str(exploit['name'])
         print "     DESCRIPTION: " + str(exploit['des'][:len(exploit['des']) - 1])
         print "     OS: " + str(exploit['os'])
         print "     EXPLOIT RANK: " + str(exploit['rank']) + " (" + str(exploit['rankNum']) + ")"
         if host['ip'] in hierarchy:
            print "  NETWORKS FOUND POST-EXPLOITATION:"
            for network in hierarchy[host['ip']]:
               print "     " + str(network)
      print "  FOUND SERVICES:"
      for s in db_s[host['ip']]:
         print "     PORT: " + str(s['port']) + ",  STATE: " + str(s['state']) + ",  NAME: " + str(s['name'] + ", INFO: " + str(s['info']))
   printDivider()
   return comp_hosts

def findExploit(ip, sessions, db_e):
   
   port = sessions[ip]['port']
   exploit = sessions[ip]['exploit']

   for i in range (len(db_e[port])):
      if db_e[port][i]['name'] == exploit:
         return db_e[port][i]

def determineOrdinalNumber(num):

   if num % 100 >= 10 and num % 100 < 20:
      return str(num) + "th"
   return str(num) + {1: "st", 2: "nd", 3: "rd"}.get(num % 10, "th")

def getSeverity(severity):
   dic = {'0': "Manual", '1': "Low", '2': "Average", '3': "Normal",
      '4': "Good", '5': "Great", '6': "Excellent"}

   return dic[severity] 

def printDivider():
   print "--------------------------------------------------"