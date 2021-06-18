import datetime
from datetime import datetime
from pytz import timezone


def giveTime():
    return datetime.now(timezone('Europe/Moscow')).replace(microsecond=0).replace(tzinfo=None)


def checkRole(current_user):
    if current_user.is_anonymous: return 'user'
    else: return current_user.role



