from flask import Blueprint

notifications = Blueprint('notifications', __name__)


def generate_notification_roomid(user_id):
    return int(str(user_id) + '000' )

from . import views, models, events