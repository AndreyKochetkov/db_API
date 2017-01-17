# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.forum.handlers.listUsers import get_list_of_users


@csrf_exempt
def listUsers(request):
    try:
        code = Code
        try:
            data = {
                "forum": str(request.GET.get("forum"))
            }
        except:
            return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads "}))

        if not data["forum"]:
            return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                       'response': 'incorrect forum format'}))

        ##################### optional arguments   #####################

        since_id = request.GET.get("since_id")
        if since_id is not None:
            data["since_id"] = since_id
        limit = request.GET.get("limit")
        if limit is not None:
            data["limit"] = limit

        order = request.GET.get("order")
        if order is not None:
            data["order"] = str(order)
        else:
            data["order"] = "desc"

        response = get_list_of_users(data)
        return HttpResponse(dumps(response))
    except:
        return HttpResponse(dumps({"code": 4, "response": "error gunicorn"}))
