# -*- coding: utf-8 -*-
from json import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.user.handlers.listFollowing import get_list_of_users


@csrf_exempt
def listFollowing(request):
    code = Code
    try:
        data = {
            "user": str(request.GET.get("user"))
        }
    except Exception as e:
        print str(e)
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads "}))

    if not data["user"]:
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
