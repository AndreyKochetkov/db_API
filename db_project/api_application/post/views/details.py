# -*- coding: utf-8 -*-
from json import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.post.handlers.details import get_detail_post


@csrf_exempt
def details(request):
    try:
        code = Code
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

        response = get_detail_post(post, related)
        return HttpResponse(dumps(response))
    except:
        return HttpResponse(dumps({"code": 4, "response": "error gunicorn"}))
