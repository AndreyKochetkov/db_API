# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.Query import Query
from api_application.user.handlers.details import get_detail_user


def unfollow_user(follower, followee):
    cursor = connection.cursor()
    code = Code

    try:
        query = Query()
        query.add_delete("follow")
        query.add_where_condition(" follower = \"{}\" and following = \"{}\" ".format(follower, followee))
        cursor.execute(query.get())

    except Exception as e:
        print str(e)
        cursor.close()
        return {'code': code.NOT_FOUND, "response": "delete failed, user  not found"}

    cursor.close()
    response = get_detail_user(follower)
    return {'code': code.OK, "response": response}
