import os
import yaml

from warflower.docker import DockerManager
from warflower.util import to_serverid

class ServerManager:
  def __init__(self):
    currdir = os.path.dirname(__file__)
    gamesdir = os.path.join(currdir, "games")
    games = os.listdir(gamesdir)

    self.all_servers = {}
    for game in games:
      gamecfgs = yaml.safe_load(open(os.path.join(gamesdir, game)))
      gamename = os.path.splitext(os.path.basename(game))[0]
      for cfg in gamecfgs:
        self.all_servers[to_serverid(gamename, cfg)] = gamecfgs[cfg]

    self.docker_mgmt = DockerManager()
    self.active_servers = {}

  def list_configs(self):
    servers = self.all_servers
    res = {}
    for serv in servers:
      if serv in self.active_servers:
        res[serv] = 1
      else:
        res[serv] = 0
    return res


  def start_server(self, serverid, rt_args={}):
    cfg = self.all_servers[serverid]

    rt_args = {**cfg["runtime_args"], **rt_args}
    self.active_servers.append(serverid)

    return self.docker_mgmt.start(cfg["image"], cfg["command"], to_serverid(game, preset)) # , **rt_args)

  def stop_server(self, serverid=None):
    return self.docker_mgmt.stop(to_serverid(game, preset))

    



if __name__ == "__main__":
  sm = ServerManager()
  import pdb; pdb.set_trace()
  pass
