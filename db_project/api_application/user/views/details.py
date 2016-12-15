# -*- coding: utf-8 -*-
from json import dumps
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.user.utils import get_user_by_email
from api_application.utils.logger import get_logger


@csrf_exempt
def details(request):
    logger = get_logger()
    logger.debug("/forum/details: \n")
    cursor = connection.cursor()
    code = Code()
    if request.method != 'GET':
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'request method should be GET'}))
    email = request.GET.get('user')
    if not email:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'user not correct'}))
    try:
        query = get_user_by_email(email)
        logger.debug(query.get())
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return HttpResponse(dumps({'code': code.NOT_FOUND,
                                       'response': 'user not found'}))
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR,
                                   'response': 'failed select user'}))

    user = cursor.fetchone()
    response = {
        "id": user[0],
        "email": user[1],
        "name": user[2],
        "username": user[3],
        "about": user[4],
        "isAnonymous": user[5],
        "following": [],
        "followers": [],
        "subscriptions": []
    }

    return HttpResponse(dumps({'code': code.OK,
                               'response': response}))
