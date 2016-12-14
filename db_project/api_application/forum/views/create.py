# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.user.utils import get_user_by_email
from api_application.forum.utils import get_forum_by_short_name


@csrf_exempt
def create(request):
    cursor = connection.cursor()
    code = Code()
    try:
        request_data = loads(request.body)
        data = (
            ["name", request_data["name"]],
            ["short_name", request_data["short_name"]],
            ["user", request_data["user"]]
        )
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))

    try:
        query = get_user_by_email(request_data["user"])
        print (query.get())
        cursor.execute(query.get())

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select user failed"}))

    try:
        if cursor.fetchone()[0]:
            pass
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.USER_EXISTS, "response": "user doesn't exists"}))
    response = {}
    try:
        query.clear()
        query.add_insert("forum", data)
        print(query.get())
        cursor.execute(query.get())

    except:
        try:
            query = get_forum_by_short_name(request_data["short_name"])
            print(query.get())
            cursor.execute(query.get())

            existed_forum = cursor.fetchone()
            cursor.close()

            return HttpResponse(dumps({'code': code.OK,
                                   'response': {
                                       'id': existed_forum[0],
                                       'short_name': existed_forum[1],
                                       'name': existed_forum[2],
                                       'user': existed_forum[3]
                                   }}))
        except:
            cursor.close()
            return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "short_name exist, name doesn't"}))
    try:
        query.clear()
        query.select_last_insert_id()
        cursor.execute(query.get())

        forum_id = cursor.fetchone()[0]
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select last id failed"}))

    response = {
        "id": forum_id,
        "name": request_data["name"],
        "short_name": request_data["short_name"],
        "user": request_data["user"]
    }

    cursor.close()
    return HttpResponse(dumps({'code': code.OK, "response": response}))
