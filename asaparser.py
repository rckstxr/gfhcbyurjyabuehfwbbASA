import re
import json

class Parser:

    def __init__(self):
        pass


    def read_asa_config(self, config_file):
        f = open(config_file, "r")
        config = f.read()
        f.close()

        return config


    def get_acl_rules_from_config(self, config_file, save_to_file=False, out_file=False):
        config = self.read_asa_config(config_file)
        acl_rules_list = re.findall(r'access-list .* extended .*\n', config)
        acl_rules_in_json = []
        for acl in acl_rules_list:
            acl = acl.split("\n")
            print(acl)
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

#        if save_to_file:
#            acl_rules_list_file = open(out_file, "w")
#            for rule in acl_rules_list:
#                acl_rules_list_file.write(rule);
#            acl_rules_list_file.close()
#            return
#        else:
#            rule_list = []
#            for rule in acl_rules_list:
#                rule_list.append(rule)
#            return rule_list


    def get_objects_from_config(self, config_file, save_to_file=False, out_file=False):
        config = self.read_asa_config(config_file)
        object_list = re.findall(r'object (?:network|service).*\n .*\n', config)
        obj_list_in_json = []
        for obj in object_list:
            obj = obj.split("\n")
            json_obj = {}
            json_obj.update({"object_type":obj[0].split(" ")[1]})
            json_obj.update({"object_name":obj[0].split(" ")[2]})
            json_obj.update({"object_rule":obj[1]})
            obj_list_in_json.append(json_obj)


        if save_to_file:
            with open(out_file, "w") as f:
                json.dump({"obj_list":obj_list_in_json}, f, indent=True)
            return

        return {"obj_list":obj_list_in_json}


    def get_object_groups_from_config(self, config_file, save_to_file=False, out_file=False):
        config = self.read_asa_config(config_file)
        object_group_list = re.findall(r'object-group.*\n( .+\n)+', config)

        group_list_in_json = []
        for groups in object_group_list:
            print(groups)
            group = groups[0]
            print(group)
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
