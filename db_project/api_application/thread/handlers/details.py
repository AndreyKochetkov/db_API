# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.thread.utils import get_query_detail_thread_by_id
from api_application.user.handlers.details import get_detail_user


def get_detail_thread(id_thread, related=None):
    if related is None:
        related = []
    cursor = connection.cursor()
    code = Code()

    try:
        if "forum" in related:
            has_forum = True
        else:
            has_forum = False
        query = get_query_detail_thread_by_id(id_thread, has_forum)
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return {'code': code.NOT_FOUND,
                    'response': 'thread not found'}
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR,
                'response': 'failed select thread'}

    thread = cursor.fetchone()


    response = {
        "id": thread[0],
        "title": thread[1],
        "slug": thread[2],
        "message": thread[3],
        "date": str(thread[4]),
        "posts": thread[5],
        "likes": thread[6],
        "dislikes": thread[7],
        "points": thread[8],
        "isClosed": bool(thread[9]),
        "isDeleted": bool(thread[10]),
        "forum": thread[11],
        "user": thread[12]
    }
    if "user" in related:
        response["user"] = get_detail_user(thread[12])
    if "forum" in related:
        response["forum"] = {
            "name": thread[13],
            "short_name": thread[14],
            "user": thread[15],
            "id": thread[16]
        }

    cursor.close()
    return {'code': code.OK,
            'response': response}
