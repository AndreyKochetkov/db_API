# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.thread.handlers.close import close_thread

@csrf_exempt
def close(request):
    logger = get_logger()
    code = Code()
    try:
        request_data = loads(request.body)
        data = {
            "thread": request_data["thread"]
        }
    except:
        logger.debug("error close thread")
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))
    try:
        data["thread"] = int(data["thread"])
    except:
        logger.debug("error close thread")
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "thread isnt int"}))

    response = close_thread(data)

    return HttpResponse(dumps(response))
