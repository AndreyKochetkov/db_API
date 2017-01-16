# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.thread.handlers.unsubscribe import unsubscribe_user


@csrf_exempt
def unsubscribe(request):
    logger = get_logger()
    code = Code()
    try:
        request_data = loads(request.body)

        user_mail = str(request_data["user"])
        thread_id = request_data["thread"]
    except:
        logger.debug("error unsub thread")
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    try:
        thread_id = int(thread_id)
    except:
        logger.debug("error unsub thread")
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "thread isnt int"}))

    response = unsubscribe_user(thread_id, user_mail)
    return HttpResponse(dumps(response))