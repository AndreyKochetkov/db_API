# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.thread.handlers.listPosts import get_list_of_posts


@csrf_exempt
def listPosts(request):
    logger = get_logger()
    code = Code()
    try:
        data = {
            "thread": str(request.GET.get("thread"))
        }
    except:
        logger.debug("error list posts thread")
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads "}))
    try:
        data["thread"] = int(data["thread"])
    except:
        logger.debug("error list posts thread")
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "thread isnt int"}))

    ##################### optional arguments   #####################

    since = request.GET.get("since")
    if since is not None:
        data["since"] = since
    limit = request.GET.get("limit")

    if limit is not None:
        try:
            data["limit"] = int(limit)
        except:
            logger.debug("error list posts thread")
            return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "limit isnt int"}))

    order = request.GET.get("order")
    if order is not None:
        data["order"] = str(order)
    else:
        data["order"] = "desc"

    sort = request.GET.get("sort")
    if sort is not None:
        data["sort"] = str(sort)
    else:
        data["sort"] = "flat"

    response = get_list_of_posts(data)
    return HttpResponse(dumps(response))
