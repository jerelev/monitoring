import logging
import config
from prometheus_client import start_http_server, Gauge

log = logging.getLogger(__name__)
PORT = config.Prometheus.SERVER_PORT

# Create Prometheus metrics to track data over time
nfs_file_write_time = Gauge('nfs_file_write_time', 'Time taken to write file')
nfs_file_read_time = Gauge('nfs_file_read_time', 'Time taken to read file')

af_download_from_01_time = Gauge('af_download_from_01_time','Time to download 100MB file from 01 Artifactory instance')
af_download_from_02_time = Gauge('af_download_from_02_time','Time to download 100MB file from 02 Artifactory instance')
af_download_from_01_speed = Gauge('af_download_from_01_speed','Speed to download 100MB file from 01 Artifactory instance')
af_download_from_02_speed = Gauge('af_download_from_02_speed','Speed to download 100MB file from 02 Artifactory instance')

def init():
  start_http_server(PORT)