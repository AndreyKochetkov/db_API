# -*- coding: utf-8 -*-
from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.validate import validate_date
from api_application.utils.logger import get_logger
from api_application.post.handlers.create import create_post


@csrf_exempt
def create(request):
    logger = get_logger()
    logger.debug("/post/create: \n")
    code = Code()
    try:

        request_data = loads(request.body)

        data = {
            "date": str(request_data["date"]),
            "thread": request_data["thread"],
            "message": request_data["message"],
            "user": request_data["user"],
            "forum": request_data["forum"]
        }
    except:
        return HttpResponse(dumps({'code': code.NOT_VALID, "response": "failed loads json"}))

    data["date"] = validate_date(data["date"])
    if not data["date"]:
        return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                   'response': 'incorrect date format'}))
    if not data["message"]:
        return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                   'response': 'incorrect message format'}))

    ##################### optional arguments   #####################
    optional_args = ['isApproved', 'isDeleted', 'isEdited', 'isHighlighted', 'isSpam']
    for optional_arg_name in optional_args:
        optional_arg_value = request_data.get(optional_arg_name)
        if optional_arg_value is not None:
            # print optional_arg_name, optional_arg_value
            if not isinstance(optional_arg_value, bool):
                return HttpResponse(dumps({'code': code.NOT_CORRECT,
                                           'response': 'optional flag should be bool'}))
            data[optional_arg_name] = optional_arg_value

    parent_id = request_data.get("parent")
    if parent_id is not None:
        if isinstance(parent_id, int):
            data["parent"] = parent_id

    response = create_post(data)
    return HttpResponse(dumps(response))
