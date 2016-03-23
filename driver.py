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
import shared

def main():

   shared.defineGlobals()
   prop_file_gen = False if "-init" in sys.argv else True

   ## user prompt
   (server_ip, server_passwd, ip_ranges, target_ip, target_location, severity, host_list) = user_input_handler.prompt_user(prop_file_gen)

   exploit_file_gen = 0

   ## tool startup
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

   print "Prop file name: " + str(shared.prop_file_name)
   
   ## scanning module (nmap and nessus)
   scan = nmap_scan.scan_location_setup()
   if scan == "y" or scan == "Y":
      nmap_scan.scan(ip_ranges)

   ## exploit gathering
   db_e = exploit_db_gen.determine_db(exploit_file_gen)
   #exploit_db_gen.print_db(db_e)

   ## service gathering
   db_s = service_db_gen.generate_db()
   #service_db_gen.print_db(db_s)

   ## host gathering
   db_h = host_db_gen.generate_db()
   #host_db_gen.print_db(db_h)

   ## attack generation
   attacks = atk_gen.determineAttackVectors(db_e, db_s, db_h, host_list)
   #atk_gen.print_attacks(attacks)
   sessions = atk_gen.generate_attacks(attacks, db_h)

   ## privilege escalation module (combine with pivoting)

   session_db = post_exploit.parseSessionData(sessions)
   print session_db
   #post_exploit.session_handler(session_db, target_ip, target_location)

'''
   ## exploit db updater
   exploit_db_gen.update_db(db_e, db_h, session_db)

   ## reporting module
   #TODO
'''
if __name__ == '__main__':
   main()
