# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.logger import get_logger
from api_application.utils.Code import Code
from api_application.thread.utils import get_query_open_thread


def open_thread(data):
    logger = get_logger()
    logger.debug(" handler open: \n")
    cursor = connection.cursor()
    code = Code()
    thread = data["thread"]
    try:
        query = get_query_open_thread(thread)
        logger.debug("\n\n get_query_open_thread(thread): " + query.get())
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "open thread failed"}

    response = {
        "thread": thread
    }

    cursor.close()
    return {'code': code.OK, "response": response}
