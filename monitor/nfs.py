import config
import logging
import json
import string
import uuid
import time
import os
import random
from utils.utils import measure_latency
from monitor import prometheus


log = logging.getLogger(__name__)

# Define the file size in bytes (100MB)
file_size = 100 * 1024 * 1024

# NFS server and file path
NFS_SERVERS = json.loads(config.Nfs.NFS_SERVERS)
NFS_WAIT_TIME = int(config.Nfs.NFS_WAIT_TIME)
MOUNT_POINT = config.Nfs.MOUNT_POINT

def init():
  while True:
    try:
      for nfs_server in NFS_SERVERS:
        log.debug('nfs_server %s', nfs_server)
        mount_point = f'{MOUNT_POINT}/{nfs_server}'
        log.info('mount_point %s', mount_point)
    
        write_time = write_file_and_measure_time(mount_point)
        random_file = random.choice(os.listdir(f'{mount_point}/tools-monitor-data/'))
        read_time = read_file_and_measure_time(f'{mount_point}/tools-monitor-data/{random_file}')

        prometheus.nfs_file_write_time.set(write_time)
        prometheus.nfs_file_read_time.set(read_time)
    except Exception as err:
      log.info(f"Unexpected {err=}, {type(err)=}")
    finally:
      log.info('Waiting %s seconds before next run', NFS_WAIT_TIME)
      time.sleep(NFS_WAIT_TIME)  # Measure each server every 30 seconds

def generate_random_data(size):
  return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

@measure_latency
def write_file_and_measure_time(directory):
  random_data = generate_random_data(file_size)
  random_filename = str(uuid.uuid4()) + '.txt'
  file_path = os.path.join(directory, random_filename)

  start_time = time.time()
  with open(file_path, 'w') as file:
    file.write(random_data)
  end_time = time.time()
  write_time = end_time - start_time
  delete_file(file_path)
  log.debug('File %s created with random data of size 100MB', file_path)
  log.debug('Write time: %s seconds', write_time)
  return write_time


@measure_latency
def read_file_and_measure_time(filename):
  log.info('Will read %s', filename)
  start_time = time.time()
  with open(filename, 'rb') as file:
    file.read()
  end_time = time.time()
  read_time = end_time - start_time
  return read_time


def delete_file(filename):
  try:
    os.remove(filename)
    log.debug('File %s deleted.', filename)
  except FileNotFoundError:
    log.debug('Could not find %s', filename)
  except Exception as err:
    log.info('Unknown error occured while removing %s', filename)
    log.info(f"Unexpected {err=}, {type(err)=}")