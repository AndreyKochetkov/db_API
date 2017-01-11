from django.db import connection

from api_application.utils.Query import Query
from api_application.utils.logger import get_logger


def create_user(data):
    logger = get_logger()
    logger.debug("def create(data)")
    cursor = connection.cursor()

    # insert user in db
    try:
        logger.debug("\n\ndata: " + str(data))
        query = Query()
        query.add_insert("user", data.items())
        logger.debug("\n  execute" + query.get() + "\n\n")
        cursor.execute(query.get())
        logger.debug("\n after execute" + query.get() + "\n\n")
    # if insert failed, that means the user with this name is existed
    except:
        cursor.close()
        return None

    # get just insert user for answer
    try:
        query.clear()
        query.select_last_insert_id()
        cursor.execute(query.get())
        logger.debug("\n" + query.get() + "\n\n")

        user_id = cursor.fetchone()[0]
        logger.debug(data["isAnonymous"])
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
        logger.debug("str(data)  " + str(response))

    # unknown error
    except:
        cursor.close()
        return None

    cursor.close()
    return response
