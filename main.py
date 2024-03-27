import logging
from utils import logger
import threading
from monitor import prometheus, artifactory, nfs

log = logging.getLogger(__name__)

if __name__ == '__main__':
  log.info('Starting Prometheus')
  # If Prom fails, the service should restart so it's not protected and not in a thread.
  prometheus.init()
  log.info('Starting Artifactory Module')
  threading.Thread(target=artifactory.init).start()
  log.info('Starting NFS Module')
  threading.Thread(target=nfs.init).start()