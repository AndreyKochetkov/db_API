# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.Query import Query
from api_application.utils.logger import get_logger


@csrf_exempt
def subscribe(request):
    logger = get_logger()
    logger.debug("/thread/subscribe: \n")
    cursor = connection.cursor()
    code = Code()
    try:
        request_data = loads(request.body)

        user_mail = request_data["user"]
        thread_id = request_data["thread"]
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    try:
        query = Query()
        query.add_insert("subscribe", (("user", user_mail), ("thread", thread_id)))
        logger.debug("insert subscribe: " + query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "insert failed"}))

    cursor.close()
    response = {
        "thread": thread_id,
        "user": user_mail
    }
    return HttpResponse(dumps({'code': code.OK, "response": response}))
