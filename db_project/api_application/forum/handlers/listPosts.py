from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.utils.validate import validate_date
from api_application.user.handlers.details import get_detail_user
from api_application.post.utils import get_query_list_posts


def get_list_of_posts(data, related):
    if related is None:
        related = []
    logger = get_logger()
    logger.debug("def get_list_of_posts(data)")
    cursor = connection.cursor()
    code = Code()
    if "since" in data:
        data["since"] = validate_date(data["since"])
    try:
        if "forum" in related:
            has_forum = True
        else:
            has_forum = False
        if "thread" in related:
            has_thread = True
        else:
            has_thread = False
        query = get_query_list_posts(data, has_forum, has_thread)
        logger.debug("list posts: " + query.get())
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
        logger.debug(type(post))
        logger.debug(str(post))
        if has_forum:
            number_of_columns_of_forum = 0
            forum = {
                "id": post[15],
                "name": post[16],
                "short_name": post[17],
                "user": post[18]
            }
        else:
            number_of_columns_of_forum = 4
            forum = post[8]

        if has_thread:
            i = number_of_columns_of_forum
            thread = {
                "id": post[19 - i],
                "title": post[20 - i],
                "slug": post[21 - i],
                "message": post[22 - i],
                "date": str(post[23 - i]),
                "posts": post[24 - i],
                "likes": post[25 - i],
                "dislikes": post[26 - i],
                "points": post[27 - i],
                "isClosed": bool(post[28 - i]),
                "isDeleted": bool(post[29 - i]),
                "forum": post[30 - i],
                "user": post[31 - i]
            }
        else:
            thread = post[9]

        if "user" in related:
            user = get_detail_user(post[10])
        else:
            user = post[10]

        response.append({
            "id": post[0],
            "message": post[1],
            "date": str(post[2]),
            "isApproved": post[3],
            "isHighlighted": bool(post[4]),
            "isEdited": bool(post[5]),
            "isSpam": bool(post[6]),
            "isDeleted": bool(post[7]),
            "forum": forum,
            "thread": thread,
            "user": user,
            "dislikes": post[11],
            "likes": post[12],
            "points": post[13],
            "parent": post[14]
        })
    logger.debug("response: " + str(response))
    return {'code': code.OK,
            'response': response}
