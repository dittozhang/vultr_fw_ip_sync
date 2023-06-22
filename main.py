import json
# from os import environ
import requests
from vultr_api import vultr_api


def get_github_nodes():
    req = requests.get("https://api.github.com/meta")
    if req.status_code != 200:
        raise Exception("[Error]Failed to retrieve the Github data.")
    return req.text


def search_fw_group_by_description(fw_groups_dict: dict,
                                   desc: str,
                                   is_fuzzy=False) -> str:
    if is_fuzzy:
        for group in fw_groups_dict["firewall_groups"]:
            if desc in group["description"]:
                return group["id"]
    else:
        for group in fw_groups_dict["firewall_groups"]:
            if desc == group["description"]:
                return group["id"]
    return ""


def search_rule_id_by_note(fw_rules_dict: dict,
                           note: str,
                           is_fuzzy=False) -> list:
    rules = []
    if is_fuzzy:
        for rule in fw_rules_dict["firewall_rules"]:
            if note in rule["notes"]:
                rules.append(rule["id"])
    else:
        for rule in fw_rules_dict["firewall_rules"]:
            if note == rule["notes"]:
                rules.append(rule["id"])
    return rules


def convert_ip_to_vultr_format(node: str,
                               protocol="TCP",
                               port=0,
                               note=None) -> dict:
    """
    No basic format checks will be performed, 
    such as disallowing the protocol to be specified as "AAA" 
    as Vultr's API already handles the validation.
    """
    rule_info = {
        "ip_type": "",
        "protocol": "",
        "subnet": "",
        "subnet_size": ""
    }
    # Mapping protocol
    rule_info["protocol"] = protocol.upper()
    # Mapping port
    if port != 0:
        rule_info.update({"port": port})
    # Mapping ip
    if ":" in node:
        rule_info["ip_type"] = "v6"
    else:
        rule_info["ip_type"] = "v4"
    rule_info["subnet"] = node.split("/")[0]
    rule_info["subnet_size"] = node.split("/")[1]
    # Mapping note
    if note is not None:
        rule_info.update({"notes": note})
    return rule_info


def main():
    token = input("token:")
    # token = environ.get("vultr_token")

    vultr = vultr_api(token)

    # block of delect old firewall rules
    # groups
    desc_of_target_group = "linked-jekyll_host"
    fw_groups_dict = json.loads(vultr.list_fw_groups())
    fw_group_id = search_fw_group_by_description(fw_groups_dict,
                                                 desc_of_target_group)
    # rules
    note_of_target_rule = "git_webhook"
    fw_rules_dict = json.loads(vultr.list_fw_rules(fw_group_id))
    rule_ids = search_rule_id_by_note(fw_rules_dict, note_of_target_rule)
    rule_ids.reverse()
    for rule_id in rule_ids:
        vultr.del_fw_rules(fw_group_id, rule_id)
    print("[Info]Old rules of the Github node has been deleted.")

    # block of add new firewall rules
    meta = json.loads(get_github_nodes())
    webhook_nodes = meta["hooks"]
    for node in webhook_nodes:
        data = convert_ip_to_vultr_format(node,
                                          "TCP",
                                          8080,
                                          note_of_target_rule)
        vultr.create_fw_rules(fw_group_id, data)
    print("[Info]New rules of the Github node has been added.")


if __name__ == "__main__":
    main()
