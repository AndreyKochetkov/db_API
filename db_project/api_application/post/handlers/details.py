# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.user.handlers.details import get_detail_user
from api_application.post.utils import get_query_detail_post_by_id


def get_detail_post(post, related=None):
    if related is None:
        related = []
    logger = get_logger()
    logger.debug(" handler thread details: \n")
    cursor = connection.cursor()
    code = Code()

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
        logger.debug("get post: " + query.get())
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

    logger.debug(str(post))
    logger.debug(type(post))

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

    if "forum" in related:
        response["forum"] = {
            "name": post[15],
            "short_name": post[16],
            "user": post[17],
            "id": post[18]
        }
    if "thread" in related:
        response["thread"] = {
            "id": post[19],
            "forum": post[20],
            "title": post[21],
            "isClosed": post[22],
            "user": post[23],
            "date": str(post[24]),
            "message": post[25],
            "slug": post[26],
            "isDeleted": post[27],
            "posts": post[28],
            "likes": post[29],
            "dislikes": post[30],
            "points": post[31]
        }
    if "user" in related:
        response["user"] = get_detail_user(response["user"])
    cursor.close()
    return {'code': code.OK,
            'response': response}
