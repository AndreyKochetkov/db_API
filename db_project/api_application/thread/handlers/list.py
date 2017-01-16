from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.utils.validate import validate_date
from api_application.thread.utils import get_query_list_threads


def get_list(data):
    logger = get_logger()
    cursor = connection.cursor()
    code = Code()
    if "since" in data:
        data["since"] = validate_date(data["since"])
    try:
        if data.get("forum"):
            query = get_query_list_threads(data, False)
        else:
            query = get_query_list_threads(data, False)
        cursor.execute(query.get())
        if not cursor.rowcount:

            cursor.close()
            return {'code': code.OK,
                    'response': []}
    except:
        cursor.close()
        logger.debug("error list thread")
        return {'code': code.UNKNOWN_ERROR,
                'response': 'failed select threads'}
    response = []
    # return {'code': code.OK,
    #       'response': response}
    for thread in cursor.fetchall():
        response.append({
            "id": thread[0],
            "title": thread[1],
            "slug": thread[2],
            "message": thread[3],
            "date": str(thread[4]),
            "posts": thread[5],
            "likes": thread[6],
            "dislikes": thread[7],
            "points": thread[8],
            "isClosed": bool(thread[9]),
            "isDeleted": bool(thread[10]),
            "forum": thread[11],
            "user": thread[12]
        })
    return {'code': code.OK,
            'response': response}
