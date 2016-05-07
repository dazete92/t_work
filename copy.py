from collections import defaultdict
from netaddr import IPNetwork, IPAddress, IPRange

def copyHostList(host_list_final, host_list, temp, hierarchy):

   for i in temp:
      b = IPNetwork(i.rsplit('.', 1)[0] + ".0").network
      #print "b: " + str(b)
      for key in hierarchy:
         for j in range (0, len(hierarchy[key])):
            #print IPNetwork(hierarchy[key][j]).network
            if b == IPNetwork(hierarchy[key][j]).network:
               host_list[i] = key

   #print host_list

   for host in host_list:
      if host not in host_list_final:
         host_list_final[host] = host_list[host]

   return host_list_final

def copyHosts(db_h_final, db_h):

   for host in db_h:
      if host not in db_h_final:
         db_h_final[host] = db_h[host]

   return db_h_final

def copyServices(db_s_final, db_s):

   for host in db_s:
      if host not in db_s_final:
         db_s_final[host] = db_s[host]

   return db_s_final

def copySessions(sessions_final, session_db):

   for session in session_db:
      if session not in sessions_final:
         sessions_final[session] = session_db[session]

   return sessions_final

def copyAttacks(attacks_final, attacks):

   for host in attacks:
      if host not in attacks_final:
         attacks_final[host] = []
         for attack in range (0, len(attacks[host])):
            attacks_final[host].append(attacks[host][attack])

   return attacks_final

def copyHierarchy(hierarchy_final, hierarchy):

   for host in hierarchy:
      if host not in hierarchy_final:
         hierarchy_final[host] = []
         for network in range (0, len(hierarchy[host])):
            hierarchy_final[host].append(hierarchy[host][network])

   return hierarchy_final

def copyIPRanges(ip_ranges_final, ip_ranges):

   ip_ranges_final.extend(ip_ranges)
   return ip_ranges_final

def copyAlteredSessions(altered_final, altered):

   altered_final.extend(altered)
   return altered_final

def copyHostsforScanning(hosts, temp):

   hosts.extend(temp)
   return hosts

def copyExploitsRun(exploitsRun_final, exploitsRun):

   for host in exploitsRun:
      if host not in exploitsRun_final:
         exploitsRun_final[host] = []
         exploitsRun_final[host].extend(exploitsRun[host])
   return exploitsRun_final

#def main():
   '''
   host_list_final = defaultdict()
   host_list = {'172.16.222.132': "root", '172.16.222.133' : "root", '172.16.222.135': "root"}
   temp = {'172.16.221.154': "root", '172.16.221.155': "root", '0.0.0.0': "root"}
   hierarchy = {'172.16.222.135': ["172.16.221.0/24"], '172.16.221.132': ["0.0.0.0/32"]}
   host_list_final = copyHostList(host_list_final, host_list, temp, hierarchy)
   #print host_list_final

   host_list = {'172.16.221.154': "root", '172.16.221.155': "root"}
   temp = {'1.2.3.4': "root", '5.6.7.8': "root", "9.9.9.1": "root"}
   hierarchy = {'172.16.221.154': ["1.2.3.0/24", "9.9.9.9/24"], '172.16.221.155': ["5.6.7.0/24"]}
   host_list_final = copyHostList(host_list_final, host_list, temp, hierarchy)
   print host_list_final
   '''

   '''
   db_h_final = defaultdict()
   db_h = {'172.16.222.128': {'ip': "172.16.222.128", 'os_name': "linux"}}
   db_h_final = copyHosts(db_h_final, db_h)
   print db_h_final

   db_h = {'172.16.221.154': {'ip': "172.16.221.154", 'os_name': "windows"}, '172.16.221.155': {'ip': "172.16.221.155", 'os_name': "linux"}}
   db_h_final = copyHosts(db_h_final, db_h)
   print db_h_final
   '''

   '''
   sessions_final = defaultdict()
   session_db = {'172.16.222.128': {'host': "172.16.222.128", \
                                    'success': "success", \
                                    'sessionNum': "1", \
                                    'user': "root", \
                                    'exploit': "exploit1", \
                                    'type': "shell"}}
   sessions_final = copyHosts(sessions_final, session_db)
   print sessions_final

   session_db = {'172.16.222.126': {'host': "172.16.222.126", \
                                    'success': "failure", \
                                    'sessionNum': "2", \
                                    'user': "root", \
                                    'exploit': "exploit2", \
                                    'type': "meterpreter"},
                 '172.16.222.125': {'host': "172.16.222.125", \
                                    'success': "failure", \
                                    'sessionNum': "3", \
                                    'user': "root", \
                                    'exploit': "exploit3", \
                                    'type': "meterpreter"}}
   sessions_final = copyHosts(sessions_final, session_db)
   print sessions_final
   '''

   '''
   attacks_final = defaultdict()
   attacks = {'1.1.1.1': ["1", "2", "3", "4", "5"],
              '2.2.2.2': ["5", "6", "7"],
              '3.3.3.3': ["8"]}
   attacks_final = copyAttacks(attacks_final, attacks)
   print attacks_final
   '''

   '''
   hierarchy_final = defaultdict()
   hierarchy = {'172.16.222.135': ["172.16.221.0/24"]}
   print copyHierarchy(hierarchy_final, hierarchy)

   hierarchy = {'172.16.221.154': ["10.1.0.0/24"]}
   print copyHierarchy(hierarchy_final, hierarchy)
   '''

   '''
   ip_ranges_final = []
   ip_ranges = ['172.16.221.0/24']
   ip_ranges_final = copyIPRanges(ip_ranges_final, ip_ranges)
   print ip_ranges_final

   ip_ranges = ['10.0.1.0/24', '5.5.5.0/16']
   ip_ranges_final = copyIPRanges(ip_ranges_final, ip_ranges)
   print ip_ranges_final
   '''

#main()
