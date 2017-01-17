# -*- coding: utf-8 -*-
from json import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.forum.handlers.details import get_detail_forum


@csrf_exempt
def details(request):
    code = Code
    if request.method != 'GET':
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'request method should be GET'}))
    short_name = request.GET.get('forum')
    if not short_name:
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'forum name not found in request'}))
    related = request.GET.get('related')

    response = get_detail_forum(short_name, related)
    return HttpResponse(dumps(response))
