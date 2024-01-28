import os
import requests 
import json

class WarflowerClient:
  def __init__(self):
    self.host = '127.0.0.1'
    self.port = 5000
    self.req = requests.Session()
    self.headers = {"Authorization": f"Bearer {os.environ['WARFLOWER_TOKEN']}"}

  def _post(self, endpoint, **kwargs):
    res = self.req.post(f"http://{self.host}:{self.port}/{endpoint}", headers=self.headers, **kwargs)
    if res.ok:
      return res.text
    raise ValueError(res.reason)

  def _get(self, endpoint, **kwargs):
    res = self.req.get(f"http://{self.host}:{self.port}/{endpoint}", headers=self.headers, **kwargs)
    if res.ok:
      return res.text
    raise ValueError(res.reason)

  def list_configs(self):
    return json.loads(self._get("list"))["data"]

  def start_server(self, serverid):
    return json.loads(self._post(f"start/{serverid}"))["ok"]

  def stop_server(self, serverid):
    return json.loads(self._post(f"stop/{serverid}"))["ok"]
