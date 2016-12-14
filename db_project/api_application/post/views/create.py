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
    option_data = []
    try:
        """
        "date": "2014-01-01 00:00:01",
        "forum": "forum2",
        "id": 1,
        "isApproved": true,
        "isDeleted": false,
        "isEdited": true,
        "isHighlighted": true,
        "isSpam": false,
        "message": "my message 1",
        "parent": null,
        "thread": 4,
        "user": "example@mail.ru"
        """
        option_data.append(["parent", request_data["parent"]])
        option_data.append(["isApproved", request_data["isApproved"]])
        option_data.append(["isHighlighted", request_data["isHighlighted"]])
        option_data.append(["isEdited", request_data["isEdited"]])
        option_data.append(["isSpam", request_data["isSpam"]])
        option_data.append(["isDeleted", request_data["isDeleted"]])
    except:
        pass

    try:

        data = [
            ("name", request_data["name"]),
            ("username", request_data["username"]),
            ("email", request_data["email"]),
            ("about", request_data["about"])
        ]
        data += option_data
        query = Query()
        query.add_insert("user", data)

        cursor.execute(query.get())

    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "insert failed"}))

    response = {}
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
            "isAnonymous": False,
            "name": request_data["name"],
            "username": request_data["username"]
        }


    except:
        cursor.close()
        return HttpResponse(dumps({'code': code.UNKNOWN_ERROR, "response": "select failed"}))

    cursor.close()
    return HttpResponse(dumps({'code': code.OK, "response": response}))
