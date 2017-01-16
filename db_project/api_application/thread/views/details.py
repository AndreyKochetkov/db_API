# -*- coding: utf-8 -*-
from json import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.thread.handlers.details import get_detail_thread


@csrf_exempt
def details(request):
    logger = get_logger()
    code = Code()
    id_thread = request.GET.get('thread')
    if not id_thread:
        logger.debug("error det thread")
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'id of thread not found in request'}))
    try:
        id_thread = int(id_thread)
    except:
        logger.debug("error det thread")
        return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                   'response': 'id isn\'t int'}))
    related = request.GET.getlist('related')
    if related:
        for value in related:
            if value != "forum":
                if value != "user":
                    logger.debug("error det thread")
                    return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                               'response': 'wrong related:' + str(related)}))

    response = get_detail_thread(id_thread, related)
    return HttpResponse(dumps(response))
