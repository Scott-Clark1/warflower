import os
import requests 
import json

class WarflowerClient:
  def __init__(self):
    self.host = '127.0.0.1'
    self.port = 5000
    self.req = requests.Session()
    self.headers = {"Authorization": f"Bearer {os.environ['WARFLOWER_TOKEN']}"}

  def _make_request(self, endpoint, **kwargs):
    res = self.req.get(f"http://{self.host}:{self.port}/{endpoint}", headers=self.headers, **kwargs)
    if res.ok:
      return res.text
    raise ValueError(res.reason)

  def list_configs(self):
    res = json.loads(self._make_request("list"))
    return res

  def start_server(self, serverid):
    objs = {"serverid" : serverid}
    res = json.loads(self._make_request("start", json=objs))
    return res
