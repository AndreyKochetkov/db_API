# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.Query import Query
from api_application.user.utils import get_query_id_user_by_email
from api_application.forum.utils import get_query_id_forum_by_short_name
from api_application.thread.utils import get_query_id_thread_by_id
from api_application.post.utils import get_query_post_by_id
from api_application.utils.logger import get_logger

"""
"isApproved": true,
"user": "example@mail.ru",
"date": "2014-01-01 00:00:01",
"message": "my message 1",
"isSpam": false,
"isHighlighted": true,
"thread": 4,
"forum": "forum2",
"isDeleted": false,
"isEdited": true
"""


def create_post(data):
    logger = get_logger()
    logger.debug("/post/create: \n")
    cursor = connection.cursor()
    code = Code()

    ###########  user verification ##############

    try:
        query = get_query_id_user_by_email(data["user"])
        logger.debug("get_user_by_email: " + query.get())
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select user failed"}

    if not cursor.rowcount:
        cursor.close()
        return {'code': code.NOT_FOUND,
                'response': 'user not found'}

    ###########  forum verification ##############

    try:
        query = get_query_id_forum_by_short_name(data["forum"])
        logger.debug("get_forum_by_short_name: " + query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select forum failed"}

    if not cursor.rowcount:
        cursor.close()
        return {'code': code.NOT_FOUND,
                'response': 'forum not found'}

    ###########  thread verification ##############

    try:
        query = get_query_id_thread_by_id(data["thread"])
        logger.debug("get_thread_by_id: " + query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select forum failed"}

    if not cursor.rowcount:
        cursor.close()
        return {'code': code.NOT_FOUND,
                'response': 'thread not found'}

    ###########  post parent verification ##############
    if data.get("parent") is not None:
        try:

            query = get_query_post_by_id(data["parent"])
            cursor.execute(query.get())
            logger.debug("get_post_by_id" + query.get())
            if not cursor.rowcount:
                cursor.close()
                return {'code': code.NOT_FOUND,
                        'response': 'post not found'}

        except:
            cursor.close()
            return {'code': code.UNKNOWN_ERROR,
                    'response': 'post select failed'}

    ######################## insert ###################


    try:
        query.clear()
        query.add_insert("post", data.items())
        logger.debug("insert post: " + query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "insert failed"}

    ######################## last post ###################
    try:
        query.clear()
        query.select_last_insert_id()
        cursor.execute(query.get())
        post_id = cursor.fetchone()[0]
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select last id failed"}


    try:
        query.clear()
        print "update post:" + query.get()
        query.add_update("thread", "posts = posts + 1")
        print query.get()
        query.add_where_condition("id = {}".format(data["thread"]))
        print query.get()
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "update posts  failed"}

    ##################### response #####################

    response = {
        "id": post_id,
        "isApproved": bool(data.get("isApproved", 0)),
        "user": data["user"],
        "date": data["date"],
        "message": data["message"],
        "isSpam": bool(data.get("isSpam", 0)),
        "isHighlighted": bool(data.get("isHighlighted", 0)),
        "thread": data["thread"],
        "forum": data["forum"],
        "isDeleted": bool(data.get("isDeleted", 0)),
        "isEdited": bool(data.get("isEdited", 0)),
        "parent": data.get("parent", None)
    }

    cursor.close()
    return {'code': code.OK, "response": response}
