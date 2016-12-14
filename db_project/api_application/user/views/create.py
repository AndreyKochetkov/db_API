# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Query import Query
from api_application.utils.Code import Code


@csrf_exempt
def create(request):
    cursor = connection.cursor()
    code = Code()
    try:
        request_data = loads(request.body)
    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads"}))
        # try:
        #   isAnonymous = request_data['isAnonymous']
    optional_data = []
    try:
        isAnonymous = request_data["isAnonymous"]
        if isinstance(isAnonymous, int):
            optional_data.append(("isAnonymous", isAnonymous))
        else:
            return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "don't correct"}))
    except:
        isAnonymous = 0

    try:
        data = [
            ("name", request_data["name"]),
            ("username", request_data["username"]),
            ("email", request_data["email"]),
            ("about", request_data["about"])
        ]
        data += optional_data
        query = Query()
        query.add_insert("user", data)

        cursor.execute(query.get())

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.USER_EXISTS, "response": "user exists"}))
    try:
        query.clear()
        columns = ["*"]
        query.add_select("user", columns)
        cursor.execute(query.get())

        query.clear()
        query.select_last_insert_id()
        cursor.execute(query.get())

        user_id = cursor.fetchone()[0]
        print (user_id)

        response = {
            "about": request_data["about"],
            "email": request_data["email"],
            "id": user_id,
            "isAnonymous": isAnonymous,
            "name": request_data["name"],
            "username": request_data["username"]
        }


    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select failed"}))

    cursor.close()
    return HttpResponse(dumps({'code': code.OK, "response": response}))
