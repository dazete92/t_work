import shared_util

def generateReport():

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