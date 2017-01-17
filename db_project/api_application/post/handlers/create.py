# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.user.utils import get_query_id_user_by_email
from api_application.forum.utils import get_query_id_forum_by_short_name
from api_application.thread.utils import get_query_id_thread_by_id, get_query_increment_posts
from api_application.post.utils import get_query_parent_thread_and_forum


def create_post(data):
    cursor = connection.cursor()
    code = Code()

    ###########  user verification ##############

    try:
        query = get_query_id_user_by_email(data["user"])
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

            query = get_query_parent_thread_and_forum(data["parent"])
            cursor.execute(query.get())
            if not cursor.rowcount:
                cursor.close()
                return {'code': code.NOT_FOUND,
                        'response': 'post not found'}

            res = cursor.fetchone()
            if res[0] != data["forum"]:
                cursor.close()
                return {'code': code.NOT_FOUND,
                        'response': 'parent is not in this forum'}
            if res[1] != data["thread"]:
                cursor.close()
                return {'code': code.NOT_FOUND,
                        'response': 'parent is not in this thread '}

        except:
            cursor.close()
            return {'code': code.UNKNOWN_ERROR,
                    'response': 'select parent post failed'}

    ######################## insert ###################


    try:
        query.clear()
        query.add_insert("post", data.items())
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
        query = get_query_increment_posts(data["thread"])
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
