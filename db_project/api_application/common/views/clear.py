from json import dumps

from django.db import connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.Query import Query
from api_application.common.utils import reset_increment


@csrf_exempt
def clear(request):
    cursor = connection.cursor()
    set_fk = "SET FOREIGN_KEY_CHECKS = 0;"
    cursor.execute(set_fk)
    query = Query()
    for table in ['follow', 'subscribe',
                  'post', 'thread', 'forum', 'user']:
        query.add_delete_clear(table)
        cursor.execute(query.get())
        cursor.execute(reset_increment(table))
    result = {"code": Code.OK,
              "response": "OK"
              }
    set_fk_1 = '''SET FOREIGN_KEY_CHECKS = 1;'''
    cursor.execute(set_fk_1)
    cursor.close()
    return HttpResponse(dumps(result))
