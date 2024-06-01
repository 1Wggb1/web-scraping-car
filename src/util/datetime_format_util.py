import datetime


def get_formatted_datetime():
    now = datetime.datetime.now()
    return now.strftime("%d_%m_%Y-%H_%M")