from django.db import connection

from api_application.user.utils import get_query_detail_user_by_email
from api_application.utils.logger import get_logger


def get_detail_user(email):
    logger = get_logger()
    logger.debug("/forum/details: \n")
    cursor = connection.cursor()
    try:
        query = get_query_detail_user_by_email(email)
        logger.debug(query.get())
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return None

    except:
        cursor.close()
        return None

    response = validate_user(cursor.fetchone())

    return response


def validate_user(user):
    if user[0] is None:
        return None
    try:
        following = user[6].split(',')
    except:
        following = []
    try:
        followers = user[7].split(',')
    except:
        followers = []
    try:
        subscriptions = user[8].split(',')
    except:
        subscriptions = []

    response = {
        "id": user[0],
        "email": user[1],
        "name": user[2],
        "username": user[3],
        "about": user[4],
        "isAnonymous": bool(user[5]),
        "following": following,
        "followers": followers,
        "subscriptions": subscriptions
    }
    return response
