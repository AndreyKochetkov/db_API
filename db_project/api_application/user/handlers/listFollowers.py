from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.user.utils import get_query_users_by_followers
from api_application.user.handlers.details import validate_user


def get_list_of_users(data):
    logger = get_logger()
    cursor = connection.cursor()
    code = Code()
    try:
        query = get_query_users_by_followers(data, True)
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return {'code': code.OK,
                    'response': []}
    except:
        logger.debug("error list followers user")
        cursor.close()
        return {'code': code.UNKNOWN_ERROR,
                'response': 'failed select users'}
    response = []
    for user in cursor.fetchall():
        response.append(validate_user(user))

    return {'code': code.OK,
            'response': response}
