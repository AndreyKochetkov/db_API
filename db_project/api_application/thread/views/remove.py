# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.thread.handlers.remove import remove_thread

@csrf_exempt
def remove(request):
    code = Code
    try:
        request_data = loads(request.body)
        data = {
            "thread": request_data["thread"]
        }
    except Exception as e:
        print str(e)
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))
    try:
        data["thread"] = int(data["thread"])
    except Exception as e:
        print str(e)
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "thread isnt int"}))

    response = remove_thread(data)

    return HttpResponse(dumps(response))
