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

