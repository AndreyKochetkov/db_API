# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.thread.handlers.open import open_thread


@csrf_exempt
def open(request):
    try:
        code = Code
        try:
            request_data = loads(request.body)
            data = {
                "thread": request_data["thread"]
            }
        except:
            return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))
        try:
            data["thread"] = int(data["thread"])
        except:
            return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "thread isnt int"}))

        response = open_thread(data)

        return HttpResponse(dumps(response))
    except:
        return HttpResponse(dumps({"code": 4, "response": "error gunicorn"}))
