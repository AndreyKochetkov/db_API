from api_application.utils.Query import Query


def get_id_user_by_email(email):
    query = Query()
    query.add_select("user", ["id"])
    query.add_where_condition("email = \"{}\"".format(email))
    return query


def get_user_by_email(email):
    query = Query()
    query.add_select("user", ["*"])
    query.add_where_condition("email = \"{}\"".format(email))
    return query


def get_user_by_id(user_id):
    query = Query()
    query.add_select("user", ["*"])
    query.add_where_condition("id = \"{}\"".format(user_id))
    return query


