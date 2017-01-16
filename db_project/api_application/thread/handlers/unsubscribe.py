# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.Query import Query
from api_application.utils.logger import get_logger


def unsubscribe_user(thread, user):
    logger = get_logger()
    cursor = connection.cursor()
    code = Code()

    try:
        query = Query()
        query.add_delete("subscribe")
        query.add_where_condition(" user = \"{}\" and thread = {} ".format(user, thread))
        cursor.execute(query.get())

    except:
        logger.debug("error unsubscribe thread")
        cursor.close()
        return {'code': code.NOT_FOUND, "response": "insert failed, user or thread not found"}

    cursor.close()
    response = {
        "thread": thread,
        "user": user
    }
    return {'code': code.OK, "response": response}
