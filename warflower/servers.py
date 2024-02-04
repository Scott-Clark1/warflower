from steam import game_servers as gs
import socket
import logging

logger = logging.getLogger("webapp")

def get_server_by_name(name):
    name = f"warflower.servers.{name}"

    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)

    if not issubclass(mod, GameServer):
      raise ValueError("Not today, satan")

    return mod


class GameServer:
  def __init__(self, serverid, host, port):
    self.serverid = serverid
    self.host = host
    self.port = port
    self.serveraddr = (host, port)

    self.player_count = 0
    self.server_name = serverid
    self.max_players = 0

  def servername(self):
    raise NotImplementedError("Not implemented")

  def playercount(self):
    raise NotImplementedError("Not implemented")

  def maxplayers(self):
    raise NotImplementedError("Not implemented")


class SteamServer(GameServer):
  def __init__(self, serverid, host, port):
    super().__init__(serverid, host, port)

    info = self._load_info()
    logger.info(info)
  
  def _load_info(self):
    info = {"players" : self.player_count, "max_players" : self.max_players, "name" : self.server_name}
    try:
      info = gs.a2s_info(self.serveraddr)
      self.info = info
    except (ConnectionRefusedError, socket.timeout) as e:
      logging.info("Data request timed out, moving on")

    return info

  def playercount(self):
    self.player_count = self._load_info()["players"]
    return self.player_count
  
  def servername(self):
    self.server_name = self._load_info()["name"]
    return self.server_name

  def maxplayers(self):
    self.max_players = self._load_info()["max_players"]
    return self.max_players

class DummyServer(GameServer):
  def __init__(self, *args, **kwargs):
    pass

  def playercount(self):
    return -1
  
  def servername(self):
    return -1

  def maxplayers(self):
    return -1
