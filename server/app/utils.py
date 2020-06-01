import datetime


def get_time():
    now = get_time()
    return datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0, 0)

def ignore_seconds(time: datetime.datetime):
    return time.replace(second=0)