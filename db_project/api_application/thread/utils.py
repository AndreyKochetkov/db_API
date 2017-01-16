from api_application.utils.Query import Query


def get_query_for_remove_thread(forum_id, is_del):
    query = Query()
    data = [("isDeleted", is_del)]
    query.add_update("thread", data)
    query.add_where_condition("id = \"{}\"".format(forum_id))
    return query


def get_query_id_thread_by_id(thread_id):
    query = Query()
    query.add_select("thread", ["id"])
    query.add_where_condition("id = \"{}\"".format(thread_id))
    return query


def get_query_decrement_posts(thread_id):
    query = Query()
    query.add_update("thread", "posts = posts - 1")
    query.add_where_condition("id = {}".format(thread_id))
    return query


def get_query_increment_posts(thread_id):
    query = Query()
    query.add_update("thread", "posts = posts + 1")
    query.add_where_condition("id = {}".format(thread_id))
    return query


def get_query_detail_thread_by_id(id_thread, has_forum):
    query = Query()

    columns = "t.*"
    if has_forum:
        columns += ", f.name f_name, f.short_name f_short_name, f.user f_user, f.id f_id"

    query.add_select("thread as t", columns)

    if has_forum:
        query.add_left_join("forum as f", "t.forum = f.short_name")

    query.add_where_condition("t.id = \"{}\"".format(id_thread))
    return query


def get_query_list_threads(data, has_forum):
    query = Query()

    columns = "t.*"
    if has_forum:
        columns += ", f.id, f.name, f.short_name, f.user"

    query.add_select("thread as t", columns)

    if has_forum:
        query.add_left_join("forum as f", "t.forum = f.short_name")

    if data.get("forum"):
        query.add_where_condition("t.forum = \"{}\"".format(data["forum"]))
    else:
        query.add_where_condition("t.user = \"{}\"".format(data["user"]))

    if "since" in data:
        query.add_more_where_condition("t.date > \"{}\"".format(data["since"]))

    query.add_order_by("t.date", data["order"])

    if "limit" in data:
        query.add_limit(data["limit"])

    return query


def get_query_close_thread(thread):
    query = Query()

    query.add_update("thread", " isClosed = 1 ")
    query.add_where_condition(" id = {}".format(thread))

    return query


def get_query_open_thread(thread):
    query = Query()

    query.add_update("thread", " isClosed = 0 ")
    query.add_where_condition(" id = {}".format(thread))

    return query


def get_query_remove_thread(thread):
    query = Query()

    query.add_update("thread", " isDeleted = 1 , posts = 0")
    query.add_where_condition(" id = {}".format(thread))

    return query


def get_query_restore_thread(thread):
    query = Query()

    query.add_update("thread as t", " isDeleted = 0 , posts = ("
                                    "select count(p.id) from post as p where p.thread = t.id)")
    query.add_where_condition(" id = {}".format(thread))

    return query


def get_query_vote_thread(thread, vote):
    if vote == 1:
        column = "likes"
        difference = " + 1 "
    elif vote == -1:
        column = "dislikes"
        difference = " - 1 "
    else:
        return None
    query = Query()
    query.add_update("thread", " {} = {} + 1, points = points {}".format(column, column, difference))
    query.add_where_condition(" id = {}".format(thread))
    return query


def get_query_update_thread(thread, message, slug):
    query = Query()
    query.add_update("thread", " message = \"{}\", slug = \"{}\" ".format(message, slug))
    query.add_where_condition(" id = {}".format(thread))

    return query

