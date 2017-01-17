# -*- coding: utf-8 -*-
from django.db import connection

from api_application.user.utils import get_query_id_user_by_email
from api_application.utils.Code import Code


def create_forum(data):
    cursor = connection.cursor()
    code = Code

    try:
        query = get_query_id_user_by_email(data["user"])
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select user failed"}

    if cursor.fetchone() is None:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "user doesn't exists"}

    try:
        query.clear()
        query.add_insert("forum", data.items())
        cursor.execute(query.get())

    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "short_name or name exist"}
    try:
        query.clear()
        query.select_last_insert_id()
        cursor.execute(query.get())

        forum_id = cursor.fetchone()[0]
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select last id failed"}

    data["id"] = forum_id

    cursor.close()
    return {'code': code.OK, "response": data}
