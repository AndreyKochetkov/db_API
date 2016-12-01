# -*- coding: utf-8 -*-
import json

from django.db import connection
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from api_application.utils.Query import Query

@csrf_exempt
def create(request):
    print("поехали")
    if request.method == "POST":
        cursor = connection.cursor()
        try:
            data = json.loads(request.body)
        except:
            cursor.close()
            return HttpResponseRedirect('/allbad')
        try:
            username = data["username"]
            about = data["about"]
            name = data["name"]
            email = data["email"]
        except:
            cursor.close()
            return HttpResponseRedirect('/allbadagain')
        #query = Query()
        #query =
        query = "INSERT INTO {} ({}) VALUES ({});".format('user', 'name, email, username, about',
                            '\"{}\", \"{}\", \"{}\", \"{}\"'.format(name, email, username, about))

        print(query)
        cursor.execute(query)
        cursor.close()
        return HttpResponseRedirect('/good')
    return HttpResponseRedirect('/oops')
