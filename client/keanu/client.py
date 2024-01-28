class WarflowerClient
  def __init__(self):
    self.host = 'localhost'
    self.port = 5000
    self.req = requests.Session()

  def _make_request(self, endpoint):
    return self.req.get(f"{host}:{port}/{endpoint}")
    
  def list_configs(self):
    self._make_request("list_configs")
