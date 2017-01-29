# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.thread.utils import get_query_vote_thread
from api_application.thread.handlers.details import get_detail_thread


def vote_thread(data):
    cursor = connection.cursor()
    code = Code
    thread = data["thread"]
    try:
        query = get_query_vote_thread(thread, data["vote"])
        if query is None:
            cursor.close()
            return {'code': code.NOT_CORRECT, "response": "vote must be 1 or -1"}
        cursor.execute(query.get())
    except Exception as e:
        print str(e)
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "vote post delete failed"}

    response = get_detail_thread(thread)

    cursor.close()
    return response
