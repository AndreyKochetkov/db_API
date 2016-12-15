# -*- coding: utf-8 -*-
from json import dumps
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.user.utils import get_user_by_id
from api_application.forum.utils import get_forum_by_short_name
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
    short_name = request.GET.get('forum')
    if not short_name:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID,
                                   'response': 'forum name not found'}))
    try:
        query = get_forum_by_short_name(short_name)
        logger.debug(query.get())
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return HttpResponse(dumps({'code': code.NOT_FOUND,
                                       'response': 'forum not found'}))
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR,
                                   'response': 'failed select forum'}))

    forum = cursor.fetchone()
    response = {
        "id": forum[0],
        "short_name": forum[1],
        "name": forum[2]
    }
    related = request.GET.get('related')
    if related:
        if related != 'user':
            cursor.close()
            return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                       'response': 'incorrect related parameter: {}'.format(related)}))
        user_id = forum[4]
        try:
            query = get_user_by_id(user_id)
            logger.debug(query.get())
            cursor.execute(query.get())
            user = cursor.fetchone()
        except:
            cursor.close()
            return HttpResponse(dumps({'code': code.UNKNOWN_ERROR,
                                       'response': ""}))
        response['user'] = {
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

    else:
        cursor.close()
    return HttpResponse(dumps({'code': code.OK,
                               'response': response}))
