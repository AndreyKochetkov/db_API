from api_application.utils.Query import Query


def get_post_by_id(post_id):
    query = Query()
    query.add_select("post", ["id"])
    query.add_where_condition("id = \"{}\"".format(post_id))
    return query
