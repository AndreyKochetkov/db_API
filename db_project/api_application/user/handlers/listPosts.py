from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.validate import validate_date
from api_application.post.utils import get_query_list_posts_by_user


def get_list_of_posts(data):

    cursor = connection.cursor()
    code = Code
    if "since" in data:
        data["since"] = validate_date(data["since"])
    try:

        query = get_query_list_posts_by_user(data)
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return {'code': code.OK,
                    'response': []}
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR,
                'response': 'failed select posts'}
    response = []
    # return {'code': code.OK,
    #       'response': response}
    for post in cursor.fetchall():

        response.append({
            "id": post[0],
            "message": post[1],
            "date": str(post[2]),
            "isApproved": post[3],
            "isHighlighted": bool(post[4]),
            "isEdited": bool(post[5]),
            "isSpam": bool(post[6]),
            "isDeleted": bool(post[7]),
            "forum": post[8],
            "thread": post[9],
            "user": post[10],
            "dislikes": post[11],
            "likes": post[12],
            "points": post[13],
            "parent": post[14]
        })
    return {'code': code.OK,
            'response': response}
