import sys
import subprocess

def scan_setup():

   command = ""
   
   while True:
      p = subprocess.Popen(['java', '-jar', 'cortana.jar', 'connect.prop', 'workspace.cna'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
      p.stdin.write("arguments %s" % "list")
      output = p.communicate()[0]
      p.stdin.close()
      print "Workspaces (* = current):"
      print output
   
      print "Commands: add delete switch proceed\n"
   
      command = raw_input("Enter command: ")
      if (command == "proceed"):
         break
      name = raw_input("Enter workspace name: ")
      p = subprocess.Popen(['java', '-jar', 'cortana.jar', 'connect.prop', 'workspace.cna'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
      p.stdin.write("arguments %s %s" % (command, name))
      p.stdin.close()
      
      
      
   
   
