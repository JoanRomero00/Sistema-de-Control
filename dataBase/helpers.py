import datetime


def fecha():
    today = datetime.datetime.now()
    return today.strftime("%Y-%m-%d %H:%M:%S")
