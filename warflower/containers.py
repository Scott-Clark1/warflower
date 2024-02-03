import docker


class DockerManager:
  def __init__(self):
    self.client = docker.from_env()

  def list(self):
    res = []
    for c in self.client.containers.list():
      res.append({"name" : c.name})
    return res

  def _get_container_by_name(self, container_name):
    containers = self.client.containers
    for c in containers.list():
      if container_name:
        if c.name == container_name:
          return c
    return None

  def stop(self, container_name=None):
    containers = self.client.containers

    if container_name:
        container = self._get_container_by_name(container_name)
        if container:
            container.stop()
    else:
      for container in containers.list():
        container.stop()

    containers.prune()
    return True 

  def start(self, image, command, name, **kwargs):
    try:
      self.client.containers.run(image, command, name=name, detach=True, **kwargs)
    except:
      return False

    return True
  
  def stats(self, image_name=None):
    container = self._get_container_by_name(image_name)
    if container:
      return container.stats(decode=None, stream=False)


if __name__ == "__main__":
  d = DockerManager()
  import pdb; pdb.set_trace()
  pass
