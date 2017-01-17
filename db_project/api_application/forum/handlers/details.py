# -*- coding: utf-8 -*-
from django.db import connection

from api_application.utils.Code import Code
from api_application.forum.utils import get_query_forum_by_short_name
from api_application.user.handlers.details import get_detail_user


def get_detail_forum(short_name, related):
    cursor = connection.cursor()
    code = Code()

    try:
        query = get_query_forum_by_short_name(short_name)
        cursor.execute(query.get())
        if not cursor.rowcount:
            cursor.close()
            return {'code': code.NOT_FOUND,
                    'response': 'forum not found'}
    except:
        cursor.close()
        return {'code': code.UNKNOWN_ERROR,
                'response': 'failed select forum'}

    forum = cursor.fetchone()
    response = {
        "id": forum[0],
        "short_name": forum[1],
        "name": forum[2],
        "user": forum[3]
    }
    if related:
        if related != 'user':
            cursor.close()
            return {'code': code.NOT_CORRECT,
                    'response': 'incorrect related parameter: {}'.format(related)}

        response['user'] = get_detail_user(forum[3])

    cursor.close()
    return {'code': code.OK,
            'response': response}
