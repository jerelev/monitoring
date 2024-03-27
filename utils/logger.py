import logging
import config
from time import gmtime, strftime


str_format = '[%(hostname)s] [%(asctime)s:%(msecs)03d] [p-%(process)05d] [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'

log_level = config.Logging.LOG_LEVEL.lower()

if log_level == 'error':
    logging_level = logging.ERROR
elif log_level == 'warning' or log_level == 'warn':
    logging_level = logging.WARNING
elif log_level == 'info':
    logging_level = logging.INFO
elif log_level == 'debug':
    logging_level = logging.DEBUG
else:
    print("ERROR: unsupported log level in logger")
    exit(1)

# if config.Logging.IS_WRITE_LOG_FILES.lower() == 'true':
#     now = strftime("%Y-%m-%d__%H-%M-%S", gmtime())
#     logging.basicConfig(
#         handlers=[
#             logging.FileHandler(f"ETL_{now}.log"),
#             logging.StreamHandler()
#         ],
#         format=str_format,
#         datefmt=date_format,
#         level=logging_level)
# else:
logging.basicConfig(
format=str_format,
datefmt=date_format,
level=logging_level)


old_factory = logging.getLogRecordFactory()

def change_record_factory():
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.hostname = config.Common.HOSTNAME
        return record
    return record_factory

logging.setLogRecordFactory(change_record_factory())