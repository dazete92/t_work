import shared_util
from collections import defaultdict

def generateReport(ip_ranges, host_list, db_h, sessions, hierarchy, 
   alteredSessions, targetTree, user_ranges, target_ip, severity, db_e, db_s, attacks_final):

   report = open("report.txt", 'w')
   printUserInformation(user_ranges, target_ip, severity, report)
   comp_hosts = printDiscoveredMachines(db_h, sessions, alteredSessions, db_e, hierarchy, db_s, attacks_final, report)
   if target_ip is not "":
      if target_ip in sessions and sessions[target_ip]['success'] == "true":
         report.write("TARGET WAS COMPROMISED:" + "\n")
      else:
         report.write("TARGET WAS EITHER NOT COMPROMISED OR NOT FOUND" + "\n")
      printTree(targetTree, target_ip, comp_hosts, report)
   else:
      report.write("TARGET WAS NOT SPECIFIED" + "\n")
   report.close()

def printTree(tree, target_ip, comp_hosts, report):

   counter = 0
   parents = []
   children = []

   report.write("Target: " + str(target_ip) + "\n")
   parents.append(target_ip)
   del tree[target_ip]
   comp_hosts["ANEX"] = {'compromised': False}

   while len(tree) > 0:
      counter += 1
      report.write(determineOrdinalNumber(counter) + " connections:" + "\n")
      for parent in parents:
         for node in tree:
            if tree[node] == parent:
               p_string = parent if comp_hosts[parent]['compromised'] == False else str(parent + "(C)")
               c_string = node if comp_hosts[node]['compromised'] == False else str(node + "(C)")
               report.write("parent: " + str(p_string) + " -> child: " + str(c_string) + "\n")
               children.append(node)

      for child in children:
         del tree[child]

      parents = children
      children = []

def printUserInformation(user_ranges, target_ip, severity, report):

   target = ""
   report.write("-----Provided IP Addresses and/or Ranges-----" + "\n")
   for i in range (0, len(user_ranges)):
      report.write(user_ranges[i] + "\n")

   if target_ip is "":
      target = "None"
   else:
      target = target_ip
   report.write("Target IP Address: " + str(target) + "\n")
   report.write("Exploit Ranking Threshold: " + str(severity) + " (" + str(getSeverity(str(severity))) + ")" + "\n")

def printDiscoveredMachines(db_h, sessions, alteredSessions, db_e, hierarchy, db_s, attacks, report):

   comp_hosts = defaultdict()

   report.write("-----Discovered Machines-------------------" + "\n")
   for h in db_h:
      host = db_h[h]
      report.write("HOST: " + host['ip'] + "\n")
      compromised = True if host['ip'] in sessions and sessions[host['ip']]['success'] == "true" else False
      report.write("  OS: " + host['os_name'] + "\n")
      report.write("  VERSION: " + host['os_version'] + "\n")
      report.write("  EXPLOITS GENERATED: " + str(len(attacks[host['ip']])) + "\n")
      if str(len(attacks[host['ip']])) != "0":
         report.write("  EXPLOITS ATTEMPTED: " + sessions[host['ip']]['numRun'] + "\n")
         report.write("  COMPROMISED: Yes\n" if compromised == True else "  COMPROMISED: No" + "\n")
         comp_hosts[host['ip']] = {'compromised': compromised}
         if compromised == True:
            exploit = findExploit(host['ip'], sessions, db_e)
            report.write("  EXPLOIT:" + "\n")
            report.write("     NAME: " + str(exploit['name']) + "\n")
            report.write("     DESCRIPTION: " + str(exploit['des'][:len(exploit['des']) - 1]) + "\n")
            report.write("     OS: " + str(exploit['os']) + "\n")
            report.write("     EXPLOIT RANK: " + str(exploit['rank']) + " (" + str(exploit['modRank']) + ")" + "\n")
            if host['ip'] in hierarchy:
               report.write("  NETWORKS FOUND POST-EXPLOITATION:" + "\n")
               for network in hierarchy[host['ip']]:
                  report.write("     " + str(network) + "\n")
         report.write("  FOUND SERVICES:" + "\n")
         for s in db_s[host['ip']]:
            report.write("     PORT: " + str(s['port']) + ",  STATE: " + str(s['state']) + ",  NAME: " + str(s['name'] + ", INFO: " + str(s['info'])) + "\n")
      else:
         comp_hosts[host['ip']] = {'compromised': compromised}
   printDivider(report)
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

def printDivider(report):
   report.write("--------------------------------------------------\n")