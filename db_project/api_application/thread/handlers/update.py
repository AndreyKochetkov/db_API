# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.thread.utils import get_query_update_thread
from api_application.thread.handlers.details import get_detail_thread


def update_thread(data):
    cursor = connection.cursor()
    code = Code
    thread = data["thread"]
    try:
        query = get_query_update_thread(thread, data["message"], data["slug"])
        cursor.execute(query.get())
    except Exception as e:
        print str(e)
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "update thread delete failed"}

    response = get_detail_thread(thread)

    cursor.close()
    return response
