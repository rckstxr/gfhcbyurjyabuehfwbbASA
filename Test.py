import re
import json
from asaparser import Parser

nParser = Parser()
#nParser.get_acl_rules_from_config(config_file="ASA1.txt", save_to_file=True, out_file="ACL.json")
#nParser.get_object_groups_from_config(config_file="ASA1.txt", save_to_file=True, out_file="Object_Groups.json")
nParser.get_objects_from_config(config_file="ASA1.txt", save_to_file=True, out_file="Objects.json")
