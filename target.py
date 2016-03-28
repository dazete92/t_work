from collections import defaultdict
from netaddr import IPNetwork, IPAddress, IPRange

def findTarget(host_list_final, target_ip):

   targetTree = defaultdict()
   treeRoot = target_ip
   children = []

   for key in host_list_final:
      if key == treeRoot:
         targetTree[key] = defaultdict()
         children.append(key)
         break

   print children

   if len(children) != 0:
      while len(children) > 0 and len(host_list_final) > 0:

         children = findImmediateChildren(host_list_final, children)

         print "children: " + str(children)

         for child in children:
            targetTree[treeRoot][child] = defaultdict()
            del host_list_final[child]

         print "host_list: " + str(host_list_final) + "\n"
   else:
      print "Target Not Found"

   print targetTree
   return targetTree

def findImmediateChildren(host_list_final, children):

   c = []

   for child in children:
      subnet = child[:child.rfind('.') + 1]

      for key in host_list_final:
         if key == child:
            c.append(host_list_final[key])
         elif key.find(subnet) != -1 or child == host_list_final[key]:
            c.append(key)

   return c

#def findChildren(host_list_final, children):



def main():

   temp = {'1.2.3.4': '172.16.221.154', '9.9.9.1': '172.16.221.154', \
      '172.16.222.133': 'root', '172.16.222.132': 'root', '172.16.222.135': 'root', \
      '172.16.221.155': '172.16.222.135', '5.6.7.8': '172.16.221.155', \
      '172.16.221.154': '172.16.222.135', '0.0.0.0': '172.16.221.132'}
   target_ip = "172.16.221.155"
   temp = findTarget(temp, target_ip)

main()