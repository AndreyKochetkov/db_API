from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.utils.validate import validate_date
from api_application.user.handlers.details import get_detail_user
from api_application.post.utils import get_query_list_posts_by_thread, get_query_list_posts_by_forum


def get_list(data):
    logger = get_logger()
    logger.debug("def get_list(data)")
    cursor = connection.cursor()
    code = Code()
    if "since" in data:
        data["since"] = validate_date(data["since"])
    try:
        if data.get("forum"):
            query = get_query_list_posts_by_forum(data, False, False)
        else:
            query = get_query_list_posts_by_forum(data, False, False)
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
    logger.debug("response: " + str(response))
    return {'code': code.OK,
            'response': response}
