import logging
import os
import sys
import yaml

from warflower.containers import DockerManager
from warflower.util import to_serverid
from warflower.servers import get_server_by_name

logger = logging.getLogger("webapp")

class ServerManager:
  def __init__(self):
    self.docker_mgmt = DockerManager()

    self.all_servers = {}
    self.games = []
    self.load_configs()
    self._refresh_active_servers()

  def _activate_server(self, serverid):
      cfg = self.all_servers[serverid]

      wrapper = cfg.get("wrapper", {})

      default_args = {"host" : "localhost", "port" : -1}

      w_class = wrapper.get("class", "DummyServer")
      w_args = wrapper.get("args", {})
      w_args = {**default_args, **w_args}

      self.active_servers[serverid] = {
        "server" : get_server_by_name(w_class)(serverid, **w_args)
      }

  def _refresh_active_servers(self):
    self.active_servers = {}
    for s in self.docker_mgmt.list():
      if s["name"] in self.all_servers:
        self._activate_server(s["name"])

  def load_configs(self):
    currdir = os.path.dirname(__file__)

    all_servers = {}
    gamesdir = os.path.join(currdir, "games")
    self.games = os.listdir(gamesdir)
    for game in self.games:
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
        serverobj = self.active_servers[serv]["server"]
        res[serv] = {
          "playercount" : serverobj.playercount(),
          "maxplayers" : serverobj.maxplayers(),
          "servername" : serverobj.servername(),
          "online" : True
        }
      else:
        res[serv] = {
          "online" : False
        }
    return res

  def list_games(self):
    self.load_configs()

    return [x.split(".")[0] for x in self.games]


  def start_server(self, serverid, rt_args={}):
    self.load_configs()
    self._activate_server(serverid)


    cfg = self.all_servers[serverid]
    rt_args = {**cfg["runtime_args"]} # , **rt_args}
    logger.info(f"Launching {serverid} with these settings:")
    logger.info(f"\t{cfg['image']}, {cfg['command']}, {serverid}")
    logger.info(f"\t{rt_args}")
    return self.docker_mgmt.start(cfg["image"], cfg["command"], serverid, **rt_args)
  
  def server_stats(self, serverid):
    self.load_configs()

    logger.info(f"Grabbing stats for {serverid}:")
    cfg = self.all_servers[serverid]

    stats = self.docker_mgmt.stats(serverid)
    cpu_usage = (stats['cpu_stats']['cpu_usage']['total_usage']
                 - stats['precpu_stats']['cpu_usage']['total_usage'])
    cpu_system = (stats['cpu_stats']['system_cpu_usage']                    
                  - stats['precpu_stats']['system_cpu_usage'])
    num_cpus = stats['cpu_stats']["online_cpus"]
    cpu_perc = (cpu_usage / cpu_system) * num_cpus * 100
    
    ret_stats = {
      "cpu" : cpu_perc,
      "mem" : stats["memory_stats"]["usage"] / stats["memory_stats"]["limit"]
    }
    return ret_stats


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
