from datetime import datetime
import pytz


def get_timezone():
    tz = pytz.timezone("America/Argentina/Buenos_Aires")
    return datetime.now(tz).astimezone(tz).replace(tzinfo=None)