from json import dumps

from django.db import connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.Query import Query


@csrf_exempt
def status(request):
    try:
        cursor = connection.cursor()
        query = Query()
        response = {}
        for table in ['post', 'thread', 'forum', 'user']:
            query.clear()
            query.add_select(table, "count(*)")
            cursor.execute(query.get())
            response[table] = cursor.fetchone()[0]
        cursor.close()
        return HttpResponse(dumps({'code': Code.OK, "response": response}))
    except:
        return HttpResponse(dumps({"code": 4, "response": "error gunicorn"}))

