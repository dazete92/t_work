import sys
import time
import exploit_db_gen
import service_db_gen
import host_db_gen
import atk_gen
import user_input_handler
import service_startup
import nmap_scan
import post_exploit
import shared_util
import copy
import report
import target
from collections import defaultdict

def main():

   shared_util.defineGlobals()
   prop_file_gen = False if "-init" in sys.argv else True

   ## user prompt
   (server_ip, server_passwd, ip_ranges, target_ip, severity) = \
      user_input_handler.prompt_user(prop_file_gen) #, host_list)

   exploit_file_gen = 0

   ## service startup
   if len(sys.argv) > 1:
      for arg in sys.argv:
         if arg == "-init":
            service_startup.init(server_ip, server_passwd)
            exploit_file_gen = 1
         if arg == "-update":
            service_startup.update()
            exploit_file_gen = 1
         if arg == "-h" or arg == "--help":
            user_input_handler.print_header()
            quit()

   print "Prop file name: " + str(shared_util.prop_file_name)

   scan = nmap_scan.scan_location_setup()
   if scan == "y" or scan == "Y":
      host_list = nmap_scan.scan(ip_ranges)
   else:
      host_list = shared_util.parseIPRanges(ip_ranges);

   ## exploit gathering
   db_e = exploit_db_gen.determine_db(exploit_file_gen)
   #exploit_db_gen.print_db(db_e)

   while True:
      ## service gathering
      db_s = service_db_gen.generate_db(host_list)
      #service_db_gen.print_db(db_s)

      ## host gathering
      db_h = host_db_gen.generate_db(host_list)
      #host_db_gen.print_db(db_h)

      ## attack generation
      attacks = atk_gen.determineAttackVectors(db_e, db_s, db_h, host_list)
      atk_gen.print_attacks(attacks)
      sessions = atk_gen.generate_attacks(attacks)

      ## privilege escalation module (combine with pivoting)
      session_db = shared_util.parseSessionData(sessions)
      print session_db

      #(session_db, new_networks, hierarchy) = post_exploit.searchForTarget(session_db, db_h, host_list)

      '''
      #scanning or leave
      if len(new_networks) > 0:

         # copy services db
         ip_ranges_final = copyIPRanges(ip_ranges_final, ip_ranges)
         db_h_final = copy.copyHosts(db_h_final, dh_h)
         sessions_final = copy.copySesssions(sessions_final, session_db)
         attacks_final = copy.copyAttacks(attacks_final, attacks)
         hierarchy_final = copyHierarchy(hierarchy_final, hierarchy)

         ip_ranges = new_networks
         temp_host_list = nmap_scan.scan(ip_ranges)
         host_list_final = copy.copyHostList(host_list_final, host_list, temp_host_list, hierarchy)
         host_list = temp_host_list.copy()

      else:
         break
      '''
      break

'''
   ## find target
   host_list_final = post_exploit.findTarget(host_list_final, target_ip)

   ## exploit db updater
   exploit_db_gen.update_db(db_e_, db_h_final, sessions_final, attacks_final)

   ## reporting module
   targetTree = target.getTargetTree(host_list_final, target_ip)
   report.generateReport(host_list_final, db_h_final, attacks_final, /
      sessions_final, hierarchy_final, targetTree)

   ## close all open sessions
   post_exploit.closeSessions(sessions_final)
'''

if __name__ == '__main__':
   main()
