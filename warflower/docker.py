import docker


class DockerManager:
  def __init__(self):
    self.client = docker.from_env()

  def list(self):
    res = []
    for c in self.client.containers.list():
      res.append({"name" : c.name})
    return res


  def stop(self, container_name=None):
    succ = False
    containers = self.client.containers
    for c in containers.list():
      if container_name:
        if c.name == container_name:
          c.stop()
          succ = True
      else:
        c.stop()
        succ = True

    containers.prune()
    return succ

  def start(self, image, command, name, **kwargs):
    try:
      self.client.containers.run(image, command, name=name, detach=True, **kwargs)
    except:
      return False

    return True
