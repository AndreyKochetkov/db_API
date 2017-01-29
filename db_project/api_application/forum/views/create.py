# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.forum.handlers.create import create_forum


@csrf_exempt
def create(request):
    code = Code
    try:
        request_data = loads(request.body)
        data = {
            "name": request_data["name"],
            "short_name": request_data["short_name"],
            "user": request_data["user"]
        }
    except:
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    response = create_forum(data)

    return HttpResponse(dumps(response))
