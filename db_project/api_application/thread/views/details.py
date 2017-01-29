# -*- coding: utf-8 -*-
from json import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.thread.handlers.details import get_detail_thread


@csrf_exempt
def details(request):
    code = Code
    id_thread = request.GET.get('thread')
    if not id_thread:
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'id of thread not found in request'}))
    try:
        id_thread = int(id_thread)
    except Exception as e:
        print str(e)
        return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                   'response': 'id isn\'t int'}))
    related = request.GET.getlist('related')
    if related:
        for value in related:
            if value != "forum":
                if value != "user":
                    return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                               'response': 'wrong related:' + str(related)}))

    response = get_detail_thread(id_thread, related)
    return HttpResponse(dumps(response))
