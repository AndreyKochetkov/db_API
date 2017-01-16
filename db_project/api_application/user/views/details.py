# -*- coding: utf-8 -*-
from json import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.user.handlers.details import get_detail_user


@csrf_exempt
def details(request):
    logger = get_logger()
    code = Code()
    if request.method != 'GET':
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'request method should be GET'}))
    email = request.GET.get('user')
    if not email:
        logger.debug("error details user")
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'user not correct'}))

    response = get_detail_user(email)
    if response is not None:
        response = str(dumps({'code': code.OK, "response": response}))
        return HttpResponse(response)
    else:
        logger.debug("error details user")
        return HttpResponse(dumps({'code': code.NOT_FOUND, "response": "user doesnt exist"}))

