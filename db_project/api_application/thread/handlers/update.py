# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.logger import get_logger
from api_application.utils.Code import Code
from api_application.thread.utils import get_query_update_thread
from api_application.thread.handlers.details import get_detail_thread


def update_thread(data):
    logger = get_logger()
    logger.debug(" update thread: \n")
    logger.debug(str(data))
    cursor = connection.cursor()
    code = Code()
    thread = data["thread"]
    try:
        query = get_query_update_thread(thread, data["message"], data["slug"])
        logger.debug("\n\n get_query_update_thread: " + query.get())
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "update thread delete failed"}

    response = get_detail_thread(thread)

    cursor.close()
    return response
