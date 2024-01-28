import os
import yaml
from warflower.docker import DockerManager

class ServerManager:
  def __init__(self):
    currdir = os.path.dirname(__file__)
    gamesdir = os.path.join(currdir, "games")
    games = os.listdir(gamesdir)
    self.all_servers = {game.split(".")[0] : yaml.safe_load(open(os.path.join(gamesdir, game))) for game in games}

    self.docker_mgmt = DockerManager()

  def list_configs(self):
    return self.all_servers

  def start_server(self, game, preset=None, rt_args={}):
    game_configs = self.all_servers[game]
    if not preset:
      preset = game_configs.keys()[0]
    cfg = game_configs[preset]

    rt_args = {**cfg["runtime_args"], **rt_args}
    return self.docker_mgmt.start(cfg["image"], serverid(game, preset), *rt_args)

  def stop_server(self, game=None, preset=None):
    if game is None and preset is None:
      self.docker_mgmt.stop()
    return self.docker_mgmt.stop(serverid(game, preset))

    



if __name__ == "__main__":
  sm = ServerManager()
  import pdb; pdb.set_trace()
  pass
