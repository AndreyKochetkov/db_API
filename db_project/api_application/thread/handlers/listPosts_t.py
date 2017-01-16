from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.post.utils import get_query_list_root_posts, get_query_list_child_posts


def get_list_posts_t(data):
    logger = get_logger()

    cursor = connection.cursor()
    code = Code()
    has_limit = data.get("limit", False)
    try:
        query = get_query_list_root_posts(data)
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return {'code': code.OK,
                    'response': []}

    except:
        cursor.close()
        logger.debug("error list posts t thread")
        return {'code': code.UNKNOWN_ERROR,
                'response': 'failed select root posts'}
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

    index_list = -1
    try:
        while index_list is not None:
            index_list += 1

            id_of_parent_post = response[index_list]["id"]

            try:
                query = get_query_list_child_posts(data, id_of_parent_post)
                cursor.execute(query.get())
                if cursor.rowcount:
                    add_child_index = index_list
                    array = cursor.fetchall()
                    for post in array:
                        add_child_index += 1
                        response.insert(add_child_index, {
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
                        if has_limit:
                            if data["limit"] < add_child_index:
                                cursor.close()
                                response = response[:data["limit"] ]
                                return {'code': code.OK,
                                        'response': response}


            except:
                logger.debug("error list posts t thread")
                cursor.close()
                return {'code': code.UNKNOWN_ERROR,
                        'response': 'failed select child posts'}
    except IndexError:
        response = response[:data["limit"] ]
        cursor.close()
        return {'code': code.OK,
                'response': response}
