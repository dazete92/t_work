from collections import defaultdict
from netaddr import IPNetwork, IPAddress, IPRange

def copyHostList(host_list_final, host_list, temp, hierarchy):

   for i in temp:
      b = IPNetwork(i.rsplit('.', 1)[0] + ".0").network
      print "b: " + str(b)
      for key in hierarchy:
         for j in range (0, len(hierarchy[key])):
            print IPNetwork(hierarchy[key][j]).network
            if b == IPNetwork(hierarchy[key][j]).network:
               host_list[i] = key

   print host_list

   for host in host_list:
      if host not in host_list_final:
         host_list_final[host] = host_list[host]

   return host_list_final

def main():
   host_list_final = defaultdict()
   host_list = {'172.16.222.132': "", '172.16.222.133' : "", '172.16.222.135': ""}
   temp = {'172.16.221.154': "", '172.16.221.155': "", '0.0.0.0': ""}
   hierarchy = {'172.16.222.135': ["172.16.221.0/24"], '172.16.221.132': ["0.0.0.0/32"]}
   host_list_final = copyHostList(host_list_final, host_list, temp, hierarchy)
   print host_list_final

   host_list = {'172.16.221.154': "", '172.16.221.155': ""}
   temp = {'1.2.3.4': "", '5.6.7.8': "", "9.9.9.1": ""}
   hierarchy = {'172.16.221.154': ["1.2.3.0/24", "9.9.9.9/24"], '172.16.221.155': ["5.6.7.0/16"]}
   host_list_final = copyHostList(host_list_final, host_list, temp, hierarchy)
   print host_list_final

main()