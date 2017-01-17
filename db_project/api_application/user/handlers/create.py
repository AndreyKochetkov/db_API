from django.db import connection

from api_application.utils.Query import Query


def create_user(data):
    cursor = connection.cursor()

    # insert user in db
    try:
        query = Query()
        query.add_insert("user", data.items())
        cursor.execute(query.get())
    # if insert failed, that means the user with this name is existed
    except:
        cursor.close()
        return None

    # get just insert user for answer
    try:
        query.clear()
        query.select_last_insert_id()
        cursor.execute(query.get())

        user_id = cursor.fetchone()[0]
        if data["isAnonymous"] == 1:
            name = None
            about = None
            username = None
        else:
            name = data["name"]
            username = data["username"]
            about = data["about"]

        response = data

        response["name"] = name
        response["username"] = username
        response["about"] = about
        response["id"] = user_id

    # unknown error
    except:
        cursor.close()
        return None

    cursor.close()
    return response
