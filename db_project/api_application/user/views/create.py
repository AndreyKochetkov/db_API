# -*- coding: utf-8 -*-
import json

from django.db import connection
from django.http import HttpResponseRedirect
from api_application.utils.Query import Query

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
            email = datap["email"]
        except:
            cursor.close()
            return HttpResponseRedirect('/allbadagain')


