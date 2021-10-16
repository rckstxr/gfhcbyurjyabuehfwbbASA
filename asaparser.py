import re
import json
import ipaddress

class Parser:

    def __init__(self):
        pass


    def read_asa_config(self, config_file):
        f = open(config_file, "r")
        config = f.read()
#        print(config)
        f.close()

        return config


    def get_acl_rules_from_config(self, config_file, save_to_file=False, out_file=False):
        config = self.read_asa_config(config_file)
        regexp = re.compile('access-list .* extended .*\n')
        acl_rules_list = regexp.findall(config)
        acl_rules_in_json = []
        for acl in acl_rules_list:
            acl = acl.split("\n")
#            print(acl)
            json_acl = {}
            json_acl.update({"ACL_name":acl[0].split(" ")[1]})
            json_acl.update({"ACL_action":acl[0].split(" ")[3]})
            json_acl.update({"ACL_rule":acl[0].split(" ")[4:-1]})
            acl_rules_in_json.append(json_acl)

        if save_to_file:
            with open(out_file, "w") as f:
                json.dump({"acl_rules_list":acl_rules_in_json}, f, indent=True)
            return

        return {"acl_rules_list":acl_rules_in_json}


    def get_objects_from_config(self, config_file, save_to_file=False, out_file=False):
        config = self.read_asa_config(config_file)
        regexp = re.compile('object (?:network|service).*\n .*\n')
        object_list = regexp.findall(config)
        obj_list_in_json = []
        for obj in object_list:
            obj = obj.split("\n")
            json_obj = {}
            json_obj.update({"object_type":obj[0].split(" ")[1]})
            json_obj.update({"object_name":obj[0].split(" ")[2]})
            json_obj.update({"object_rule":obj[1]})
            obj_list_in_json.append(json_obj)
            if obj[1].split(" ")[1] == "host":
                json_obj.update({"object_rule_type":"host"})
                json_obj.update({"object_rule_target":obj[1].split(" ")[-1]})
            if obj[1].split(" ")[1] == "service":
                json_obj.update({"object_rule_type":"service"})
                json_obj.update({"object_rule_service_type": obj[1].split(" ")[2]})
                json_obj.update({"object_rule_target":obj[1].split(" ")[-2]})
            if obj[1].split(" ")[1] == "range":
                json_obj.update({"object_rule_type": "range"})
                json_obj.update({"object_rule_target1":obj[1].split(" ")[2]})
                json_obj.update({"object_rule_target2":obj[1].split(" ")[3]})
                #need to modify range and write hosts to json separately

        if save_to_file:
            with open(out_file, "w") as f:
                json.dump({"obj_list":obj_list_in_json}, f, indent=True)
            return

        return {"obj_list":obj_list_in_json}


    def get_object_groups_from_config(self, config_file, save_to_file=False, out_file=False):
        config = self.read_asa_config(config_file)
        regexp = re.compile('object-group.*\n(?: .+\n)+')
        object_group_list = regexp.findall(config)
        group_list_in_json = []
        for group in object_group_list:
#            print(group)
            json_group = {}
            group = group.split("\n")
            json_group.update({"group_type":group[0].split(" ")[1]})
            json_group.update({"group_name":group[0].split(" ")[2]})
            json_group.update({"group_rules":[]})

            for rule in group[1:-1:]:
                json_group["group_rules"].append(rule)

            group_list_in_json.append(json_group)

        if save_to_file:
            with open(out_file, "w") as f:
                json.dump({"group_list":group_list_in_json}, f, indent=True)
            return

        return {"group_list":group_list_in_json}
