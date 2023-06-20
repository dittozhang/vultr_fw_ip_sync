import json
import requests
from vultr_api import vultr_api

key = input("key:")

vultr = vultr_api(key)

def get_github_nodes():
    req = requests.get("https://api.github.com/meta")
    return req.text

def check_ip_version(ip:str) -> str:
    if ":" in ip:
        return "v6"
    else:
        return "v4"

meta = json.loads(get_github_nodes())
webhook_nodes = meta["hooks"]