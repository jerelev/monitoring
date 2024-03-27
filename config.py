"""
Tools Monitoring Config
"""
import os

from dotenv import load_dotenv

load_dotenv()

class Common:
    HOSTNAME = os.environ['HOSTNAME']
class Nfs:
    NFS_SERVERS = os.environ['NFS_SERVERS']
    NFS_WAIT_TIME = os.environ['NFS_WAIT_TIME']
    MOUNT_POINT = os.environ['MOUNT_POINT']
class Artifactory:
    AF_SERVER_01 = os.environ['AF_SERVER_01']
    AF_SERVER_02 = os.environ['AF_SERVER_02']
    ARTIFACTORY_100MB_FILE_PATH = os.environ['AF_FILE']
    LOCAL_FILENAME = "/tmp/random_data_100MB.txt"
class Logging:
    LOG_LEVEL = os.environ['LOG_LEVEL']
class Prometheus:
    SERVER_PORT = 8000