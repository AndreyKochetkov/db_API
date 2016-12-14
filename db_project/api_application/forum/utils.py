from api_application.utils.Query import Query


def get_forum_by_short_name(short_name):
    query = Query()
    query.add_select("forum", ["id"])
    query.add_where_condition("short_name = \"{}\"".format(short_name))
    return query
