# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.thread.utils import get_query_restore_thread
from api_application.post.utils import get_query_restore_post_for_thread


def restore_thread(data):
    cursor = connection.cursor()
    code = Code()
    thread = data["thread"]
    try:
        query = get_query_restore_thread(thread)
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "restore thread failed"}
    try:
        query = get_query_restore_post_for_thread(thread)
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "restore post failed"}

    response = {
        "thread": thread
    }

    cursor.close()
    return {'code': code.OK, "response": response}
