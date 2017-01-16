# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.post.handlers.vote import vote_post


@csrf_exempt
def vote(request):
    logger = get_logger()
    code = Code()
    try:
        request_data = loads(request.body)
        data = {
            "post": request_data["post"],
            "vote": request_data["vote"]
        }
    except:
        logger.debug("error vote post")
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))
    try:
        data["post"] = int(data["post"])
    except:
        logger.debug("error vote post")
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "post isnt int"}))
    try:
        data["vote"] = int(data["vote"])
    except:
        logger.debug("error vote post")
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "vote isnt int"}))

    response = vote_post(data)

    return HttpResponse(dumps(response))
