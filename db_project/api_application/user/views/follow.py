# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.user.utils import get_user_by_email
from api_application.utils.logger import get_logger


@csrf_exempt
def follow(request):
    logger = get_logger()
    logger.debug("/user/follow: \n")
    cursor = connection.cursor()
    code = Code()
    try:
        request_data = loads(request.body)

        follower = request_data["follower"]
        followee = request_data["followee"]
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    ########### user follower verification ##############

    try:
        query = get_user_by_email(follower)
        logger.debug("follower get_user_by_email: " + query.get())
        cursor.execute(query.get())
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select user failed"}))

    if not cursor.rowcount:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_FOUND,
                                   'response': 'user not found'}))

    follower = cursor.fetchone()[1]

    ########### user followee verification ##############

    try:
        query = get_user_by_email(followee)
        logger.debug("followee get_user_by_email: " + query.get())
        cursor.execute(query.get())
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select user failed"}))

    if not cursor.rowcount:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_FOUND,
                                   'response': 'user not found'}))

    followee = cursor.fetchone()[1]

    try:
        query.clear()
        query.add_insert("follow", (("follower", follower), ("following", followee)))
        logger.debug("insert follow: " + query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "insert failed"}))

    cursor.close()
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
    return HttpResponse(dumps({'code': code.OK, "response (заглушка)": response}))
