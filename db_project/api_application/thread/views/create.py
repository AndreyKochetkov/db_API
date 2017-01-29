# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.thread.handlers.create import create_thread


@csrf_exempt
def create(request):
    code = Code
    try:
        request_data = loads(request.body)

        data = {
            "forum": request_data["forum"],
            "title": request_data["title"],
            "isClosed": bool(request_data["isClosed"]),
            "user": request_data["user"],
            "message": request_data["message"],
            "slug": request_data["slug"],
            "date": request_data["date"]
        }
    except Exception as e:
        print str(e)
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))


        ##################### optional arguments / remove thread  #####################
    try:
        is_deleted = bool(request_data["isDeleted"])
        data["isDeleted"] = is_deleted
        # TODO: check to no bool
    except Exception as e:
        print str(e)
        pass

    response = create_thread(data)
    return HttpResponse(dumps(response))
