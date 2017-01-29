from django.db import connection

from api_application.utils.Code import Code
from api_application.user.handlers.details import validate_user
from api_application.thread.utils import get_query_list_threads
from api_application.utils.validate import validate_date
from api_application.user.handlers.details import get_detail_user


def get_list_of_threads(data, related):
    if related is None:
        related = []
    cursor = connection.cursor()
    code = Code
    if "since" in data:
        data["since"] = validate_date(data["since"])
    try:
        if "forum" in related:
            has_forum = True
        else:
            has_forum = False
        query = get_query_list_threads(data, has_forum)
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return {'code': code.OK,
                    'response': []}
    except Exception as e:
        print str(e)
        cursor.close()
        return {'code': code.UNKNOWN_ERROR,
                'response': 'failed select threads'}
    response = []
    for thread in cursor.fetchall():
        if has_forum:
            forum = {
                "id": thread[13],
                "name": thread[14],
                "short_name": thread[15],
                "user": thread[16]
            }
        else:
            forum = thread[11]

        if "user" in related:
            user = get_detail_user(thread[12])
        else:
            user = thread[12]

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
            "forum": forum,
            "user": user
        })

    return {'code': code.OK,
            'response': response}
