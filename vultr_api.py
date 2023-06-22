import json
import requests


class vultr_api:
    """
    Created for a personal project and only implemented the methods I needed.
    """
    def __init__(self, api_token):
        self.api_token = api_token
        # check token
        req = self._call_api("GET", "account")
        if req.status_code != 200:
            print(f"[Error] Token invalid.\nMsg:{req.text}")
            raise

    def _call_api(self, method, endpoint, data=None):
        method = method.upper()
        API_ENTRANCE_URL = "https://api.vultr.com/v2/"
        headers = {
            "Authorization": "Bearer " + self.api_token
        }
        if method == "GET":
            return requests.get(API_ENTRANCE_URL + endpoint, headers=headers)
        elif method == "POST":
            return requests.post(API_ENTRANCE_URL + endpoint,
                                 headers=headers,
                                 data=json.dumps(data))
        elif method == "DELETE":
            return requests.delete(API_ENTRANCE_URL + endpoint,
                                   headers=headers,
                                   data=json.dumps(data))
        else:
            raise Exception("[Error] This method is not supported currently")

    def list_account_info(self) -> str:
        endpoint = "account"
        req = self._call_api("GET", endpoint)
        return req.text

    def list_fw_groups(self) -> str:
        endpoint = "firewalls"
        req = self._call_api("GET", endpoint)
        return req.text

    def list_fw_rules(self, gw_group_id: str) -> str:
        endpoint = f"firewalls/{gw_group_id}/rules"
        req = self._call_api("GET", endpoint)
        return req.text

    def create_fw_rules(self, gw_group_id: str, rule_info: dict) -> str:
        endpoint = f"firewalls/{gw_group_id}/rules"
        req = self._call_api("POST", endpoint, rule_info)
        return req.text

    def del_fw_rules(self, gw_group_id: str, rule_id: int) -> str:
        endpoint = f"firewalls/{gw_group_id}/rules/{rule_id}"
        req = self._call_api("DELETE", endpoint, rule_id)
        return req.text
