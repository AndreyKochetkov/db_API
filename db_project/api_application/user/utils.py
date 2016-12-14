from api_application.utils.Query import Query


def get_user_by_email(email):
    query = Query()
    query.add_select("user", ["id"])
    query.add_where_condition("email = \"{}\"".format(email))
    print(email)
    return query
