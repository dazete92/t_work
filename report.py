import shared_util

def generateReport(ip_ranges, host_list, db_h, sessions, hierarchy, 
   alteredSessions, targetTree, user_ranges, target_ip, severity, db_e, db_s):

   printUserInformation(user_ranges, target_ip, severity)
   printDiscoveredMachines(db_h, sessions, alteredSessions, db_e, hierarchy, db_s)
   if target_ip is not "":
      if target_ip in sessions:
         print "TARGET WAS COMPROMISED:"
         printTree(targetTree, target_ip)
      else:
         print "TARGET WAS EITHER NOT COMPROMISED OR NOT FOUND"
   else:
      print "TARGET WAS NOT SPECIFIED"

def printTree(tree, target_ip):

   counter = 0
   parents = []
   children = []

   print "Target: " + str(target_ip)
   parents.append(target_ip)
   del tree[target_ip]

   while len(tree) > 0:
      counter += 1
      print determineOrdinalNumber(counter) + " connections:"
      for parent in parents:
         for node in tree:
            if tree[node] == parent:
               print "parent: " + str(parent) + " -> child: " + str(node)
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

def printDiscoveredMachines(db_h, sessions, alteredSessions, db_e, hierarchy, db_s):

   print "-----Discovered Machines-------------------"
   for h in db_h:
      host = db_h[h]
      print "HOST: " + host['ip']
      compromised = host['ip'] in sessions
      print "  OS: " + host['os_name']
      print "  VERSION: " + host['os_version']
      print "  COMPROMISED: " + "Yes" if compromised == True else "No"
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
         print "     PORT: " + str(s['port']) + ",  PROTOCOL: " + str(s['protocol']) + ",  STATE: " + str(s['state']) + ",  NAME: " + str(s['name'])
   printDivider()

def findExploit(ip, sessions, db_e):
   
   port = sessions[ip]['port']
   exploit = sessions[ip]['exploit']

   for i in range (len(db_e[port])):
      if db_e[port][i]['name'] == exploit:
         return db_e[port][i]

def getSeverity(severity):
   dic = {'0': "Manual", '1': "Low", '2': "Average", '3': "Normal",
      '4': "Good", '5': "Great", '6': "Excellent"}

   return dic[severity] 

def printDivider():
   print "--------------------------------------------------"