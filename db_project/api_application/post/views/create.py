# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.user.utils import get_query_id_user_by_email
from api_application.forum.utils import get_query_id_forum_by_short_name
from api_application.utils.validate import validate_date
from api_application.thread.utils import get_query_for_remove_thread, get_query_id_thread_by_id
from api_application.post.utils import get_post_by_id
from api_application.utils.logger import get_logger
"""
"isApproved": true,
"user": "example@mail.ru",
"date": "2014-01-01 00:00:01",
"message": "my message 1",
"isSpam": false,
"isHighlighted": true,
"thread": 4,
"forum": "forum2",
"isDeleted": false,
"isEdited": true
"""



@csrf_exempt
def create(request):
    logger = get_logger()
    logger.debug("/post/create: \n")
    cursor = connection.cursor()
    code = Code()
    try:
        request_data = loads(request.body)
        date = request_data["date"]
        thread_id = request_data["thread"]
        message = request_data["message"]
        user = request_data["user"]
        forum = request_data["forum"]
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads json"}))

    ###########  user verification ##############

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
        query = get_query_id_forum_by_short_name(forum)
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

    ###########  thread verification ##############

    try:
        query = get_query_id_thread_by_id(thread_id)
        logger.debug("get_thread_by_id: " + query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select forum failed"}))

    if not cursor.rowcount:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_FOUND,
                                   'response': 'thread not found'}))
    thread_id = cursor.fetchone()[0]

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

        ##################### optional arguments   #####################
    query_params = {}
    optional_args = ['isApproved', 'isDeleted', 'isEdited', 'isHighlighted', 'isSpam']
    for optional_arg_name in optional_args:
        optional_arg_value = request_data.get(optional_arg_name)
        if optional_arg_value is not None:
            # print optional_arg_name, optional_arg_value
            if not isinstance(optional_arg_value, bool):
                cursor.close()
                return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                           'response': 'optional flag should be bool'}))
            query_params[optional_arg_name] = optional_arg_value

    parent_id = request_data.get("parent")
    if parent_id is not None:
        try:
            if not isinstance(parent_id, int):
                cursor.close()
                return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                           'response': 'optional parent should be int'}))
            query = get_post_by_id(parent_id)
            cursor.execute(query.get())
            logger.debug("get_post_by_id" + query.get())
            if not cursor.rowcount:
                cursor.close()
                return HttpResponse(dumps({'code': code.NOT_FOUND,
                                           'response': 'post not found'}))
            query_params["parent"] = cursor.fetchone()[0]

        except:
            cursor.close()
            return HttpResponse(dumps({'code': code.UNKNOWN_ERROR,
                                       'response': '??'}))

    ######################## insert ###################

    request_data["date"] = date
    try:
        query.clear()
        request_data.update(query_params)
        query.add_insert("post", request_data.items())
        logger.debug("insert post: " + query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "insert failed"}))

    ######################## last post ###################
    try:
        query.clear()
        query.select_last_insert_id()
        cursor.execute(query.get())

        post_id = cursor.fetchone()[0]
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select last id failed"}))



    ##################### response #####################

    response = {
        "isApproved": request_data.get("isApproved", 0),
        "user": user,
        "date": date,
        "message": message,
        "isSpam": request_data.get("isSpam", 0),
        "isHighlighted": request_data.get("isHighlighted", 0),
        "thread": thread_id,
        "forum": forum,
        "isDeleted": request_data.get("isDeleted", 0),
        "isEdited": request_data.get("isEdited", 0)
    }

    cursor.close()
    return HttpResponse(dumps({'code': code.OK, "response": response}))
