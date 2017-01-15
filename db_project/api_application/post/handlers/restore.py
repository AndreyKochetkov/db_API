# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.logger import get_logger
from api_application.utils.Code import Code
from api_application.post.utils import get_query_restore_post, get_query_thread_of_post_by_id
from api_application.thread.utils import get_query_increment_posts


def restore_post(data):
    logger = get_logger()
    logger.debug(" restore post: \n")
    cursor = connection.cursor()
    code = Code()
    post = data["post"]
    try:
        query = get_query_restore_post(post)
        logger.debug("\n\n get_query_restore_post: " + query.get())
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "update post delete failed"}

    try:
        query = get_query_thread_of_post_by_id(post)
        cursor.execute(query.get())
        thread = cursor.fetchone()[0]
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select last id failed"}

    try:
        query = get_query_increment_posts(thread)
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "update thread failed"}

    response = {
        "post": post
    }

    cursor.close()
    return {'code': code.OK, "response": response}
