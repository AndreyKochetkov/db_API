# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.post.handlers.remove import remove_post


@csrf_exempt
def remove(request):
    code = Code
    try:
        request_data = loads(request.body)
        data = {
            "post": request_data["post"]
        }
    except Exception as e:
        print str(e)
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))
    try:
        data["post"] = int(data["post"])
    except Exception as e:
        print str(e)
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "post isnt int"}))

    response = remove_post(data)

    return HttpResponse(dumps(response))
