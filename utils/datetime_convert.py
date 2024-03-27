from datetime import datetime

TIME_FORMAT_WITH_FRACTION = '%Y-%m-%dT%H:%M:%S.%f'


def datetime_to_bo_format(datetime: datetime) -> str:
    return datetime.strftime(TIME_FORMAT_WITH_FRACTION)[:-3] + 'Z'