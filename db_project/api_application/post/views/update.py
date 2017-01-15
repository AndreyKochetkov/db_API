# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.post.handlers.update import update_post


@csrf_exempt
def update(request):
    logger = get_logger()
    logger.debug("/post/update: \n")
    code = Code()
    try:
        request_data = loads(request.body)
        data = {
            "post": request_data["post"],
            "message": request_data["message"]
        }
    except:
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))
    try:
        data["post"] = int(data["post"])
    except:
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "post isnt int"}))
    try:
        data["message"] = str(data["message"])
    except:
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "message isnt correct"}))

    response = update_post(data)

    return HttpResponse(dumps(response))
