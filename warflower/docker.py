import docker


class DockerManager:
  def __init__(self):
    self.client = docker.from_env()

  def stop(self, container_name=None):
    containers = self.client.containers
    for c in containers:
      if container_name:
        if c.name == container_name:
          c.stop()
      else:
        c.stop()

  def start(self, image, command, name, **kwargs):
    self.client.run(image, command, name=name, **kwargs)
