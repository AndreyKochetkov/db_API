# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.logger import get_logger
from api_application.utils.Code import Code
from api_application.thread.utils import get_query_restore_thread
from api_application.post.utils import get_query_restore_post_for_thread


def restore_thread(data):
    logger = get_logger()
    logger.debug(" handler restore: \n")
    cursor = connection.cursor()
    code = Code()
    thread = data["thread"]
    try:
        query = get_query_restore_thread(thread)
        logger.debug("\n\n  get_query_restore_thread: " + query.get())
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "restore thread failed"}
    try:
        query = get_query_restore_post_for_thread(thread)
        logger.debug("\n\n  get_query_restore_post_for_thread: " + query.get())
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "restore post failed"}

    response = {
        "thread": thread
    }

    cursor.close()
    return {'code': code.OK, "response": response}
