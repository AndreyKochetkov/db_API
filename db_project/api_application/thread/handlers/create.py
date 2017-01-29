# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.user.utils import get_query_id_user_by_email
from api_application.forum.utils import get_query_id_forum_by_short_name
from api_application.utils.validate import validate_date
from api_application.thread.utils import get_query_for_remove_thread


def create_thread(data):
    cursor = connection.cursor()
    code = Code

    ########### user verification ##############

    try:
        query = get_query_id_user_by_email(data["user"])
        cursor.execute(query.get())
    except Exception as e:
        print str(e)
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select user failed"}

    if not cursor.rowcount:
        cursor.close()
        return {'code': code.NOT_FOUND,
                'response': 'user not found'}

    user_id = cursor.fetchone()[0]

    ###########  forum verification ##############

    try:
        query = get_query_id_forum_by_short_name(data["forum"])
        cursor.execute(query.get())

    except Exception as e:
        print str(e)
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select forum failed"}

    if not cursor.rowcount:
        cursor.close()
        return {'code': code.NOT_FOUND,
                'response': 'forum not found'}
    forum_id = cursor.fetchone()[0]

    ##################### validate arguments  #####################

    data["date"] = validate_date(data["date"])
    if not data["date"]:
        cursor.close()
        return {'code': code.NOT_CORRECT,
                'response': 'incorrect date format'}

    if not data["message"]:
        cursor.close()
        return {'code': code.NOT_CORRECT,
                'response': 'incorrect message format'}

    if not data["slug"]:
        cursor.close()
        return {'code': code.NOT_CORRECT,
                'response': 'slug should not be empty'}

    if not data["title"]:
        cursor.close()
        return {'code': code.NOT_CORRECT,
                'response': 'title should not be empty'}

    ######################## insert without optional arguments ###################

    try:
        query.clear()
        query.add_insert("thread", data.items())
        cursor.execute(query.get())

    except Exception as e:
        print str(e)
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "insert failed"}
    try:
        query.clear()
        query.select_last_insert_id()
        cursor.execute(query.get())

        thread_id = cursor.fetchone()[0]
    except Exception as e:
        print str(e)
        cursor.close()
        return {'code': code.UNKNOWN_ERROR, "response": "select last id failed"}

        ##################### optional arguments / remove thread  #####################
    try:
        if isinstance(data["is_deleted"], bool):
            try:
                query = get_query_for_remove_thread(forum_id, data["is_deleted"])
                cursor.execute(query.get())

            except:
                cursor.close()
                return {'code': code.UNKNOWN_ERROR, "response": "remove thread failed"}
    except Exception as e:
        print str(e)
        data["is_deleted"] = 0

    ##################### response #####################
    response = {
        "date": data["date"],
        "forum": data["forum"],
        "id": thread_id,
        "isClosed": data["isClosed"],
        "isDeleted": data["is_deleted"],
        "message": data["message"],
        "slug": data["slug"],
        "title": data["title"],
        "user": data["user"]
    }

    cursor.close()
    return {'code': code.OK, "response": response}
