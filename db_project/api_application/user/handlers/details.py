from django.db import connection

from api_application.user.utils import get_query_detail_user_by_email


def get_detail_user(email):
    cursor = connection.cursor()
    try:
        query = get_query_detail_user_by_email(email)
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return None

    except Exception as e:
        print str(e)
        cursor.close()
        return None

    response = validate_user(cursor.fetchone())

    return response


def validate_user(user):
    if user[0] is None:
        return None
    try:
        following = user[6].split(',')
    except Exception as e:
        print str(e)
        following = []
    try:
        followers = user[7].split(',')
    except Exception as e:
        print str(e)
        followers = []
    try:
        subscriptions = user[8].split(',')
        new_subs = []
        for sub in subscriptions:
            new_subs.append(int(sub))
    except Exception as e:
        print str(e)
        new_subs = []

    response = {
        "id": user[0],
        "email": user[1],
        "name": user[2],
        "username": user[3],
        "about": user[4],
        "isAnonymous": bool(user[5]),
        "following": following,
        "followers": followers,
        "subscriptions": new_subs
    }
    return response
