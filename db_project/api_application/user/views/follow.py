# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.user.handlers.follow import follow_user


@csrf_exempt
def follow(request):
    code = Code
    try:
        request_data = loads(request.body)

        follower = request_data["follower"]
        followee = request_data["followee"]
    except Exception as e:
        print str(e)
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    response = follow_user(follower, followee)
    return HttpResponse(dumps(response))
