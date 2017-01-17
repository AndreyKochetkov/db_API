# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.thread.utils import get_query_remove_thread
from api_application.post.utils import get_query_remove_post_for_thread


def remove_thread(data):
    cursor = connection.cursor()
    code = Code
    thread = data["thread"]
    try:
        query = get_query_remove_thread(thread)
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "remove thread failed"}
    try:
        query = get_query_remove_post_for_thread(thread)
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "remove post failed"}

    response = {
        "thread": thread
    }

    cursor.close()
    return {'code': code.OK, "response": response}
