from requests import get, post, put, delete
from settings.setting import setting

class VPN:
    def __init__(self, json_data= {}):
        self.json_data = json_data
        self.api_url = f"https://{setting['bot_server_url']}:{setting['bot_server_port']}/{setting['bot_server_api']}"
        self.keys = "/access-keys/"
    
    def create_key(self, key_id=-1):
        if(key_id != -1):
            res = put(self.api_url+self.keys+str(key_id), json=self.json_data, verify=False)
        else:
            res = post(self.api_url+self.keys, json=self.json_data, verify=False)
        # print(res.json())
        return res.json()
    
    def get_key(self, key_id):
        res = get(self.api_url+self.keys+str(key_id), verify=False)
        # print(res.json())
        return res.json()
    
    def get_keys(self):
        res = get(self.api_url+self.keys, verify=False)
        # print(res.json())
        return res.json()
    
    def delete_key(self, key_id):
        res = delete(self.api_url+self.keys+str(key_id), verify=False)
        # print(res.json())
        return res.text
    def set_name(self, key_id, name):
        res = put(self.api_url+self.keys+str(key_id)+f"/name", json={"name":name}, verify=False)
        return res.text
    def set_limit(self, key_id, bytes:int=10737418240):
        res = put(self.api_url+self.keys+str(key_id)+f"/data-limit", json={"limit": {"bytes": bytes}}, verify=False)
        return res.text
    def set_all_access_key_limit(self, bytes:int=10737418240):
        res = put(self.api_url+"/server/access-key-data-limit", json={"limit": {"bytes": bytes}}, verify=False)
        if(res.status_code == 204):
            print("Success")
        return res.text
   