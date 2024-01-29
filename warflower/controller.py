import logging
import os
import sys
import yaml

from warflower.docker import DockerManager
from warflower.util import to_serverid

logger = logging.getLogger("webapp")

class ServerManager:
  def __init__(self):
    self.all_servers = {}
    self.load_configs()

    self.docker_mgmt = DockerManager()
    self.active_servers = {}

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

    logger.info("OK, TRYING THIS SHIT OUT!")
    logger.info(f"{cfg['image']}, {cfg['command']}, {serverid}")
    logger.error(f"{rt_args}")
    self.docker_mgmt.start(cfg["image"], cfg["command"], serverid, **rt_args)
    return True

  def stop_server(self, serverid=None):
    logger.info("Shutting down " + serverid)
    self.load_configs()

    self.docker_mgmt.stop(serverid)
    self.active_servers.pop(serverid, None)
    return True


if __name__ == "__main__":
  sm = ServerManager()
