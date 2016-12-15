# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Query import Query
from api_application.utils.Code import Code
from api_application.utils.logger import get_logger


@csrf_exempt
def create(request):
    logger = get_logger()
    logger.debug("/user/create: \n")
    cursor = connection.cursor()
    code = Code()
    try:
        request_data = loads(request.body)
        data = [
            ("name", request_data["name"]),
            ("username", request_data["username"]),
            ("email", request_data["email"]),
            ("about", request_data["about"])
        ]
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    try:
        isAnonymous = request_data["isAnonymous"]
        if isinstance(isAnonymous, int):
            data.append(("isAnonymous", isAnonymous))
        else:
            return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "don't correct"}))
    except:
        data.append(("isAnonymous", 0))

    try:
        logger.debug("\n\ndata: " + str(data))
        query = Query()
        query.add_insert("user", data)
        cursor.execute(query.get())
        logger.debug("\n" + query.get() + "\n\n")
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.USER_EXISTS, "response": "user exists"}))

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
            "isAnonymous": data[4][1],
            "user": user_id
        }

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select failed"}))

    cursor.close()
    return HttpResponse(dumps({'code': code.OK, "response": response}))
