# -*- coding: utf-8 -*-
from json import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.post.handlers.list import get_list


@csrf_exempt
def list(request):
    code = Code()
    data = None
    if request.GET.get("forum"):
        data = {
            "forum": request.GET.get("forum")
        }
    if request.GET.get("thread"):
        data = {
            "thread": request.GET.get("thread")
        }
    if data is None:
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "data in None "}))
    if len(data) > 1:
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "forum or thread only"}))

    ##################### optional arguments   #####################

    since = request.GET.get("since")
    if since is not None:
        data["since"] = since
    limit = request.GET.get("limit")
    if limit is not None:
        data["limit"] = limit

    order = request.GET.get("order")
    if order is not None:
        data["order"] = str(order)
    else:
        data["order"] = "desc"

    response = get_list(data)
    return HttpResponse(dumps(response))
