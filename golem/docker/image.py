from client import local_client
from docker import errors
import logging

log = logging.getLogger(__name__)

class DockerImage(object):

    def __init__(self, repository=None, image_id=None, tag=None):
        self.repository = repository
        self.id = image_id
        self.tag = tag if tag else "latest"
        self.name = "{}:{}".format(self.repository, self.tag)

    def __repr__(self):
        return "DockerImage(repository=%r, image_id=%r, tag=%r)" % (self.repository, self.id, self.tag)

    def is_available(self):
        client = local_client()
        try:
            if self.id:
                info = client.inspect_image(self.id)
                return self.name in info["RepoTags"]
            else:
                info = client.inspect_image(self.name)
                return self.id is None or info["Id"] == self.id
        except errors.NotFound:
            log.debug('DockerImage NotFound', exc_info=True)
            return False
        except errors.APIError:
            log.debug('DockerImage APIError', exc_info=True)
            if self.tag is not None:
                return False
            raise
        except ValueError:
            log.debug('DockerImage ValueError', exc_info=True)
            return False
