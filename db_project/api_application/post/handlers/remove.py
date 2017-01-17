# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.post.utils import get_query_remove_post_for_id, get_query_thread_of_post_by_id
from api_application.thread.utils import get_query_decrement_posts


def remove_post(data):
    cursor = connection.cursor()
    code = Code
    post = data["post"]
    try:
        query = get_query_remove_post_for_id(post)
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "update post delete failed"}

    try:
        query = get_query_thread_of_post_by_id(post)
        cursor.execute(query.get())
        thread = cursor.fetchone()[0]
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select last id failed"}

    try:
        query = get_query_decrement_posts(thread)
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "update thread failed"}

    response = {
        "post": post
    }

    cursor.close()
    return {'code': code.OK, "response": response}
