# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.logger import get_logger
from api_application.utils.Code import Code
from api_application.thread.utils import get_query_close_thread


def close_thread(data):
    logger = get_logger()
    cursor = connection.cursor()
    code = Code()
    thread = data["thread"]
    try:
        query = get_query_close_thread(thread)
        cursor.execute(query.get())
    except:
        logger.debug("error close thread")
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "close thread failed"}

    response = {
        "thread": thread
    }

    cursor.close()
    return {'code': code.OK, "response": response}
