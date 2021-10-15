import re
import json
from asaparser import Parser

new_parser = Parser()
new_parser.get_acl_rules_from_config(config_file="ASA1.txt", save_to_file=True, out_file="ACL.json")
#new_parser.get_object_groups_from_config(config_file="ASA1.txt", save_to_file=True, out_file="ACL.json")