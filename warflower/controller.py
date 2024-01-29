import logging
import os
import sys
import yaml

from warflower.docker import DockerManager
from warflower.util import to_serverid

logger = logging.getLogger("webapp")

class ServerManager:
  def __init__(self):
    self.docker_mgmt = DockerManager()

    self.all_servers = {}
    self.load_configs()
    self._refresh_active_servers()

  def _refresh_active_servers(self):
    self.active_servers = {}
    for s in self.docker_mgmt.list():
      if s["name"] in self.all_servers:
        self.active_servers[s["name"]] = {}

  def load_configs(self):
    currdir = os.path.dirname(__file__)

    all_servers = {}
    gamesdir = os.path.join(currdir, "games")
    games = os.listdir(gamesdir)
    for game in games:
      if game[-5:] != ".yaml":
        continue
      gamecfgs = yaml.safe_load(open(os.path.join(gamesdir, game)))
      gamename = os.path.splitext(os.path.basename(game))[0]
      for cfg in gamecfgs:
        all_servers[to_serverid(gamename, cfg)] = gamecfgs[cfg]
    self.all_servers = all_servers

  def list_configs(self):
    self.load_configs()

    servers = self.all_servers
    res = {}

    self._refresh_active_servers()
    for serv in servers:
      if serv in self.active_servers:
        res[serv] = 1
      else:
        res[serv] = 0
    return res


  def start_server(self, serverid, rt_args={}):
    self.load_configs()

    logger.info(f"Launching {serverid} with these rtargs:")
    cfg = self.all_servers[serverid]

    rt_args = {**cfg["runtime_args"]} # , **rt_args}
    self.active_servers[serverid] = {}

    logger.info(f"Launching {serverid} with these rtargs:")
    logger.info(f"{cfg['image']}, {cfg['command']}, {serverid}")
    logger.error(f"{rt_args}")
    return self.docker_mgmt.start(cfg["image"], cfg["command"], serverid, **rt_args)

  def stop_server(self, serverid=None):
    logger.info("Shutting down " + serverid)
    self.load_configs()

    res = self.docker_mgmt.stop(serverid)
    if res:
      if serverid:
        self.active_servers.pop(serverid, None)
      else:
        self.active_servers = {}

    return res


if __name__ == "__main__":
  sm = ServerManager()
