# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Query import Query
from api_application.utils.Code import Code
from api_application.user.utils import get_id_user_by_email
from api_application.forum.utils import get_id_forum_by_short_name
from api_application.utils.validate import validate_date
from api_application.thread.utils import remove_thread
from api_application.utils.logger import get_logger


@csrf_exempt
def create(request):
    logger = get_logger()
    logger.debug("/thread/create: \n")
    cursor = connection.cursor()
    code = Code()
    try:
        request_data = loads(request.body)

        forum = request_data["forum"]
        title = request_data["title"]
        isClosed = bool(request_data["isClosed"])  # validate
        user = request_data["user"]
        message = request_data["message"]
        slug = request_data["slug"]
        date = request_data["date"]
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    ########### user verification ##############

    try:
        query = get_id_user_by_email(user)
        logger.debug("get_user_by_email: " + query.get())
        cursor.execute(query.get())
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select user failed"}))

    if not cursor.rowcount:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_FOUND,
                                   'response': 'user not found'}))

    user_id = cursor.fetchone()[0]

    ###########  forum verification ##############

    try:
        query = get_id_forum_by_short_name(forum)
        logger.debug("get_forum_by_short_name: " + query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select forum failed"}))

    if not cursor.rowcount:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_FOUND,
                                   'response': 'forum not found'}))
    forum_id = cursor.fetchone()[0]

    ##################### validate arguments  #####################

    date = validate_date(date)
    if not date:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                   'response': 'incorrect date format'}))

    if not message:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                   'response': 'incorrect message format'}))

    if not slug:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                   'response': 'slug should not be empty'}))

    if not title:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                   'response': 'title should not be empty'}))

    ######################## insert without optional arguments ###################

    request_data["date"] = date
    request_data["isClosed"] = isClosed
    try:
        query.clear()
        query.add_insert("thread", request_data.items())
        logger.debug(query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "insert failed"}))
    try:
        query.clear()
        query.select_last_insert_id()
        cursor.execute(query.get())

        thread_id = cursor.fetchone()[0]
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select last id failed"}))

        ##################### optional arguments / remove thread  #####################
    try:
        is_deleted = request_data["isDeleted"]
        if is_deleted is not None:
            is_deleted = bool(is_deleted)
            try:
                query = remove_thread(forum_id, is_deleted)
                logger.debug("\n\nremove_thread: " + query.get())
                cursor.execute(query.get())

            except:
                cursor.close()
                return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "remove thread failed"}))
    except:
        is_deleted = 0

    ##################### response #####################
    response = {
        "date": date,
        "forum": forum,
        "id": thread_id,
        "isClosed": isClosed,
        "isDeleted": is_deleted,
        "message": message,
        "slug": slug,
        "title": title,
        "user": user
    }

    cursor.close()
    return HttpResponse(dumps({'code': code.OK, "response": response}))
