from api_application.utils.Query import Query


def remove_thread(forum_id, isDel):
    query = Query()
    query.add_update("thread", "isDeleted", isDel)
    query.add_where_condition("id = \"{}\"".format(forum_id))
    return query


def get_thread_by_id(thread_id):
    query = Query()
    query.add_select("thread", ["id"])
    query.add_where_condition("id = \"{}\"".format(thread_id))
    return query
