from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.validate import validate_date
from api_application.post.utils import get_query_list_posts_by_forum
from api_application.thread.handlers.listPosts_pt import get_list_posts_pt
from api_application.thread.handlers.listPosts_t import get_list_posts_t


def get_list_of_posts(data):
    cursor = None
    code = Code
    if "since" in data:
        data["since"] = validate_date(data["since"])
    try:
        if data["sort"] == "parent_tree":
            response = get_list_posts_pt(data)
            return response
        elif data["sort"] == "tree":
            response = get_list_posts_t(data)
            return response
        else:
            cursor = connection.cursor()
            query = get_query_list_posts_by_forum(data, False, False)
            cursor.execute(query.get())
            if not cursor.rowcount:
                cursor.close()
                return {'code': code.OK,
                        'response': []}
    except Exception as e:
        print str(e)
        if cursor:
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
