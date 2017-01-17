# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.user.utils import get_query_update_user
from api_application.user.handlers.details import get_detail_user


def update_user(data):
    cursor = connection.cursor()
    code = Code
    user = data["user"]
    try:
        query = get_query_update_user(user, data["about"], data["name"])
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "update user delete failed"}

    response = get_detail_user(user)

    cursor.close()
    return response
