# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.user.handlers.details import get_detail_user
from api_application.post.utils import get_query_detail_post_by_id


def get_detail_post(post, related=None):
    if related is None:
        related = []
    cursor = connection.cursor()
    code = Code

    try:
        if "forum" in related:
            has_forum = True
        else:
            has_forum = False
        if "thread" in related:
            has_thread = True
        else:
            has_thread = False
        query = get_query_detail_post_by_id(post, has_forum, has_thread)
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return {'code': code.NOT_FOUND,
                    'response': 'post not found'}
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR,
                'response': 'failed select post'}

    post = cursor.fetchone()


    response = {
        "id": post[0],
        "message": post[1],
        "date": str(post[2]),
        "isApproved": post[3],
        "isHighlighted": bool(post[4]),
        "isEdited": bool(post[5]),
        "isSpam": bool(post[6]),
        "isDeleted": bool(post[7]),
        "forum": post[8],
        "thread": post[9],
        "user": post[10],
        "dislikes": post[11],
        "likes": post[12],
        "points": post[13],
        "parent": post[14]
    }
    if has_forum:
        dif = 0
    else:
        dif = 4
    if "forum" in related:
        response["forum"] = {
            "name": post[15],
            "short_name": post[16],
            "user": post[17],
            "id": post[18]
        }
    if "thread" in related:
        response["thread"] = {
            "id": post[19 - dif],
            "forum": post[20 - dif],
            "title": post[21 - dif],
            "isClosed": post[22 - dif],
            "user": post[23 - dif],
            "date": str(post[24 - dif]),
            "message": post[25 - dif],
            "slug": post[26 - dif],
            "isDeleted": post[27 - dif],
            "posts": post[28 - dif],
            "likes": post[29 - dif],
            "dislikes": post[30 - dif],
            "points": post[31 - dif]
        }
    if "user" in related:
        response["user"] = get_detail_user(response["user"])
    cursor.close()
    return {'code': code.OK,
            'response': response}
