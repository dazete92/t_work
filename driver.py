import sys
import time
import exploit_db_gen
import service_db_gen
import host_db_gen
import atk_gen
import user_input_handler
import tool_startup

def main():
   '''
   ## user prompt
   user_input_handler.print_header()
   (server_ip, server_passwd, ip_ranges, target_ip, target_path, severity) = user_input_handler.prompt_user()
   print server_ip, server_passwd, ip_ranges, target_ip, target_path, severity

   ## tool startup
   tool_startup.init(server_ip, server_passwd)
   '''
   ## scanning module (nmap and nessus)
   #TODO

   ## exploit gathering
   db_e = exploit_db_gen.generate_db()
   #exploit_db_gen.print_db(db_e)
   
   ## service gathering
   db_s = service_db_gen.generate_db()
   #service_db_gen.print_db(db_s)

   ## host gathering
   db_h = host_db_gen.generate_db()
   #host_db_gen.print_db(db_h)

   ## attack generation
   attacks = atk_gen.determineAttackVectors(db_e, db_s, db_h)
   #atk_gen.print_attacks(attacks)
   atk_gen.generate_attacks(attacks, db_h)

   ## session handling module
   #TODO
   
   ## privilege escalation module (combine with pivoting)
   #TODO
   
   ## reporting module
   #TODO
   
if __name__ == '__main__':
   main()
