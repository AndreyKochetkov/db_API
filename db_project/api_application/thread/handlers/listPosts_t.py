from django.db import connection

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.post.utils import get_query_list_root_posts, get_query_list_child_posts


def get_list_posts_t(data):
    logger = get_logger()
    logger.debug("def get_list_posts_t(data)")
    cursor = connection.cursor()
    code = Code()
    has_limit = data.get("limit", False)
    find_end = False
    try:
        query = get_query_list_root_posts(data)
        logger.debug("get_query_list_root_posts: " + query.get())
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return {'code': code.OK,
                    'response': []}

    except:
        cursor.close()
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
    logger.debug("len(response) = " + str(len(response)))
    logger.debug("str(has_limit) = " + str(has_limit))

    index_list = -1
    try:
        while index_list is not None:
            index_list += 1

            id_of_parent_post = response[index_list]["id"]

            logger.debug("current index_list :")
            logger.debug(str(index_list))
            logger.debug("current len(response) :")
            logger.debug(str(len(response)))
            logger.debug("current id_of_parent_post :")
            logger.debug(str(id_of_parent_post))
            try:
                query = get_query_list_child_posts(data, id_of_parent_post)
                logger.debug("get_query_list_child_posts(data, id_of_parent_post): " + query.get())
                cursor.execute(query.get())
                if cursor.rowcount:
                    logger.debug("no empty set")
                    add_child_index = index_list
                    array = cursor.fetchall()
                    for post in array:
                        add_child_index += 1
                        logger.debug("current add_child_index :")
                        logger.debug(str(add_child_index))
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
                                logger.debug("add_child_index:")
                                logger.debug(add_child_index)
                                logger.debug("len(response):")
                                logger.debug(len(response))
                                logger.debug("data[limit]")
                                logger.debug(data["limit"])
                                cursor.close()
                                logger.debug("response")
                                logger.debug(str(response))
                                response = response[:data["limit"] ]
                                return {'code': code.OK,
                                        'response': response}

                else:
                    logger.debug("empty set")

            except:
                cursor.close()
                return {'code': code.UNKNOWN_ERROR,
                        'response': 'failed select child posts'}
    except IndexError:
        logger.debug("response")
        logger.debug(str(response))
        response = response[:data["limit"] ]
        cursor.close()
        return {'code': code.OK,
                'response': response}
