from json import dumps, loads
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api_application.utils.Code import Code
from api_application.utils.logger import get_logger
from api_application.user.handlers.create import create_user


@csrf_exempt
def create(request):
    logger = get_logger()
    logger.debug("/user/create: \n")
    code = Code()
    # try to load needed data from request
    try:
        request_data = loads(request.body)
        # using a list for data
        data = {
            "name": request_data["name"],
            "username": request_data["username"],
            "email": request_data["email"],
            "about": request_data["about"]
        }
    # except if we have invalid json
    except:
        return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "failed loads"}))

    # try to get optional parameter
    try:
        logger.debug("try get anon")
        isAnonymous = request_data["isAnonymous"]
        if isinstance(isAnonymous, bool):
            logger.debug("is bool")
            data["isAnonymous"] = isAnonymous
            if isAnonymous is True:
                data = {
                    "email": request_data["email"],
                    "isAnonymous": 1
                }
        else:
            return HttpResponse(dumps({'code': code.NOT_CORRECT, "response": "don't correct"}))
    # except if we have not an optional parameter
    except:
        data["isAnonymous"] = 0

    # insert user in db
    response = create_user(data)
    logger.debug("response" + str(response))
    if response is not None:
        return HttpResponse(dumps({'code': code.OK, "response": response}))
    else:
        return HttpResponse(dumps({'code': code.USER_EXISTS, "response": "insert error"}))
