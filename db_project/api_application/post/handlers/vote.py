# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.post.utils import get_query_vote_post
from api_application.post.handlers.details import get_detail_post


def vote_post(data):
    cursor = connection.cursor()
    code = Code()
    post = data["post"]
    try:
        query = get_query_vote_post(post, data["vote"])
        if query is None:
            cursor.close()
            return {'code': code.NOT_CORRECT, "response": "vote must be 1 or -1"}
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "vote post delete failed"}

    response = get_detail_post(post)

    cursor.close()
    return response
