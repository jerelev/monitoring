import logging
import config
import datetime, time
import requests
import os
from monitor import prometheus
from monitor.nfs import delete_file
from utils.utils import measure_latency

log = logging.getLogger(__name__)

AF_SERVER_02 = config.Artifactory.AF_SERVER_02
AF_SERVER_01 = config.Artifactory.AF_SERVER_01
ARTIFACTORY_100MB_FILE_PATH = config.Artifactory.ARTIFACTORY_100MB_FILE_PATH
LOCAL_FILENAME = config.Artifactory.LOCAL_FILENAME

def init():
  #do a try except and wait 30sec without raise
  log.info('AF_SERVER_02 is %s', AF_SERVER_02)
  log.info('AF_SERVER_01 is %s', AF_SERVER_01)
  while True:
    try:
      TIME_02 , SPEED_02 = download_from_af(AF_SERVER_02)
      TIME_01 , SPEED_01 = download_from_af(AF_SERVER_01)
      prometheus.af_download_from_02_time.set(TIME_02)
      prometheus.af_download_from_02_speed.set(SPEED_02)
      prometheus.af_download_from_01_time.set(TIME_01)
      prometheus.af_download_from_01_speed.set(SPEED_01)
    except Exception as err:
      log.info(f"Unexpected {err=}, {type(err)=}")
    finally:
      wait_for_time()

def wait_for_time():
  while datetime.datetime.now().second not in [0, 30]:
    time.sleep(1)


@measure_latency
def download_from_af(server):
  
  log.info('Downloading from %s', server)
  
  URL = f'https://{server}/{ARTIFACTORY_100MB_FILE_PATH}'
   

  start_time = time.time()
  response = requests.get(URL, stream=True, timeout=300)

  if response.status_code == 200:
    with open(LOCAL_FILENAME, 'wb') as file:
      for chunk in response.iter_content(chunk_size=1024):
        if chunk:
          file.write(chunk)
  else:
    log.info("Failed to download file")

  end_time = time.time()
  download_time = end_time - start_time
  file_size = os.path.getsize(LOCAL_FILENAME)
  download_speed = file_size / download_time / (1024 * 1024)  # in MB/s

  delete_file(LOCAL_FILENAME)

  log.info('Download time : %s seconds', download_time)
  log.info('Download speed: %s MB/s', download_speed)
  return download_time, download_speed