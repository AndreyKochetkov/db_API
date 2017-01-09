# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.utils.Query import Query


@csrf_exempt
def follow(request):
    logger = get_logger()
    logger.debug("/user/follow: \n")
    cursor = connection.cursor()
    code = Code()
    try:
        request_data = loads(request.body)

        follower = request_data["follower"]
        followee = request_data["followee"]
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    try:
        query = Query()
        query.add_insert("follow", (("follower", follower), ("following", followee)))
        logger.debug("insert follow: " + query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "insert failed"}))

    cursor.close()
    user = cursor.fetchone()
    response = {

    }
    return HttpResponse(dumps({'code': code.OK, "response (заглушка)": response}))
