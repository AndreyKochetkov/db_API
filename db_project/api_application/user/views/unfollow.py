# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.user.handlers.unfollow import unfollow_user


@csrf_exempt
def unfollow(request):
    logger = get_logger()
    code = Code()
    try:
        request_data = loads(request.body)

        follower = request_data["follower"]
        followee = request_data["followee"]
    except:
        logger.debug("error unfollow user v")
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    response = unfollow_user(follower, followee)
    return HttpResponse(dumps(response))
