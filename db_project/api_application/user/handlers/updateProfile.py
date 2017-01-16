# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.logger import get_logger
from api_application.utils.Code import Code
from api_application.user.utils import get_query_update_user
from api_application.user.handlers.details import get_detail_user


def update_user(data):
    logger = get_logger()
    logger.debug(" update_user: \n")
    logger.debug(str(data))
    cursor = connection.cursor()
    code = Code()
    user = data["user"]
    try:
        query = get_query_update_user(user, data["about"], data["name"])
        logger.debug("\n\n get_query_update_user: " + query.get())
        cursor.execute(query.get())
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "update user delete failed"}

    response = get_detail_user(user)

    cursor.close()
    return response
