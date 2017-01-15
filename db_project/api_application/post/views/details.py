# -*- coding: utf-8 -*-
from json import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.post.handlers.details import get_detail_post

@csrf_exempt
def details(request):
    logger = get_logger()
    logger.debug("/post/details: \n")
    code = Code()
    if request.method != 'GET':
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'request method should be GET'}))
    post = request.GET.get('post')
    if not post:
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'id of post not found in request'}))
    try:
        post = int(post)
    except:
        return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                   'response': 'id isn\'t int'}))
    related = request.GET.getlist('related')
    if related:
        logger.debug("\n\n\n ! related: ")
        logger.debug(related)

    response = get_detail_post(post, related)
    return HttpResponse(dumps(response))

