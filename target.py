from collections import defaultdict
from netaddr import IPNetwork, IPAddress, IPRange

def getTargetTree(host_list_final, target_ip):

   targetTree = defaultdict()
   treeRoot = target_ip
   children = []

   for key in host_list_final:
      if key == treeRoot:
         targetTree[key] = "root"
         children.append(key)
         break

   #print children

   if len(children) != 0:
      while len(children) > 0 and len(host_list_final) > 0:

         (targetTree, children, flag) = findImmediateChildren(host_list_final, children, targetTree)

         #print "\nchildren: " + str(children)

         if flag:
            del host_list_final[treeRoot]

         for child in children:
            if child != "root":
               del host_list_final[child]

         #print "\nhost_list: " + str(host_list_final)
         #print "\ntargetTree: " + str(targetTree) + "\n"

   return targetTree

def findImmediateChildren(host_list_final, children, targetTree):

   c = []
   flag = False

   for child in children:
      subnet = child[:child.rfind('.') + 1]
      if subnet == "":
         subnet = "null"
      for key in host_list_final:
         #print child, key, key.find(subnet), host_list_final[key]
         if key == child:
            #print "if"
            flag = True
            c.append(host_list_final[key])
            targetTree[host_list_final[key]] = child
         elif key.find(subnet) != -1 or child == host_list_final[key]:
            #print "elif"
            c.append(key)
            targetTree[key] = child

   #print c
   return (targetTree, c, flag)

'''
def main():

   temp = {'1.2.3.4': '172.16.221.154', '9.9.9.1': '172.16.221.154', \
      '172.16.222.133': 'root', '172.16.222.132': 'root', '172.16.222.135': 'root', \
      '172.16.221.155': 'root', '5.6.7.8': '172.16.221.155', \
      '172.16.221.154': '172.16.222.135', '0.0.0.0': '172.16.222.132'}
   target_ip = "172.16.221.155"
   tree = getTargetTree(temp, target_ip)
   printTree(tree, target_ip)

main()
'''