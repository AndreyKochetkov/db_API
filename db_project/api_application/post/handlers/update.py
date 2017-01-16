# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.logger import get_logger
from api_application.utils.Code import Code
from api_application.post.utils import get_query_update_post
from api_application.post.handlers.details import get_detail_post


def update_post(data):
    logger = get_logger()
    cursor = connection.cursor()
    code = Code()
    post = data["post"]
    try:
        query = get_query_update_post(post, data["message"])
        cursor.execute(query.get())
    except:
        logger.debug("error update post")
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "update post delete failed"}

    response = get_detail_post(post)

    cursor.close()
    return response
