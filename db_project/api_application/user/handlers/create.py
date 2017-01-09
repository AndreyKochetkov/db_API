# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Query import Query
from api_application.utils.Code import Code
from api_application.utils.logger import get_logger


def create_user(data):
    logger = get_logger()
    logger.debug("def create(data)")
    cursor = connection.cursor()
    code = Code()

    # insert user in db
    try:
        logger.debug("\n\ndata: " + str(data))
        query = Query()
        query.add_insert("user", data)
        cursor.execute(query.get())
        logger.debug("\n" + query.get() + "\n\n")
    # if insert failed, that means the user with this name is existed
    except:
        cursor.close()
        return None

    # get just insert user for answer
    try:
        query.clear()
        query.select_last_insert_id()
        cursor.execute(query.get())
        logger.debug("\n" + query.get() + "\n\n")

        user_id = cursor.fetchone()[0]

        response = {
            "name": data[0][1],
            "username": data[1][1],
            "email": data[2][1],
            "about": data[3][1],
            "isAnonymous": bool(data[4][1]),
            "id": user_id
        }

    # unknown error
    except:
        cursor.close()
        return None

    cursor.close()
    return response
