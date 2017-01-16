# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.user.handlers.updateProfile import update_user


@csrf_exempt
def updateProfile(request):
    logger = get_logger()
    logger.debug("updateProfile: \n")
    code = Code()
    try:
        request_data = loads(request.body)
        data = {
            "user": request_data["user"],
            "about": request_data["about"],
            "name": request_data["name"],
        }
    except:
        logger.debug("error update user v")
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    try:
        data["user"] = str(data["user"])
    except:
        logger.debug("error update user v")
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "message isnt correct"}))
    try:
        data["name"] = str(data["name"])
    except:
        logger.debug("error update user v")
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "slug isnt correct"}))
    try:
        data["about"] = str(data["about"])
    except:
        logger.debug("error update user v")
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "slug isnt correct"}))

    response = update_user(data)

    return HttpResponse(dumps({'code': code.OK, "response": response}))
