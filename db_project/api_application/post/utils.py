from api_application.utils.Query import Query
from api_application.utils.logger import get_logger


def get_query_id_post_by_id(post_id):
    query = Query()
    query.add_select("post", ["id"])
    query.add_where_condition("id = \"{}\"".format(post_id))
    return query


def get_query_parent_thread_and_forum(post):
    query = Query()
    query.add_select("post", "forum, thread ")
    query.add_where_condition("id = \"{}\"".format(post))
    return query


def get_query_thread_of_post_by_id(post_id):
    query = Query()
    query.add_select("post", ["thread"])
    query.add_where_condition("id = \"{}\"".format(post_id))
    return query


def get_query_detail_post_by_id(id_post, has_forum, has_thread):
    query = Query()

    columns = 'p.id, p.message, p.date, p.isApproved, p.isHighlighted, p.isEdited, p.isSpam, ' \
              'p.isDeleted, p.forum, p.thread, p.user, p.dislikes, p.likes, p.points, p.parent'
    if has_forum:
        columns += ", f.name f_name, f.short_name f_short_name, f.user f_user, f.id f_id"

    if has_thread:
        columns += ', t.id, t.forum, t.title, t.isClosed, ' \
                   't.user, t.date, t.message, t.slug, t.isDeleted, ' \
                   't.posts, t.likes , t.dislikes , t.points '

    query.add_select("post as p", columns)

    if has_forum:
        query.add_left_join("forum as f", "p.forum = f.short_name")

    if has_thread:
        query.add_left_join("thread as t", "p.thread = t.id")
    query.add_where_condition("p.id = \"{}\"".format(id_post))

    return query


def get_query_list_posts_by_forum(data, has_forum, has_thread):
    query = Query()
    columns = "p.id, p.message, p.date, p.isApproved, p.isHighlighted, p.isEdited, p.isSpam,   " \
              "p.isDeleted, p.forum, p.thread, p.user, p.dislikes, p.likes,  p.points, p.parent"
    if has_forum:
        columns += ", f.id, f.name, f.short_name, f.user"
    if has_thread:
        columns += ", t.id, t.title, t.slug, t.message, t.date, " \
                   "t.posts, t.likes, t.dislikes, t.points, " \
                   "t.isClosed, t.isDeleted, t.forum, t.user"

    query.add_select("post as p", columns)

    if has_forum:
        query.add_left_join("forum as f", "p.forum = f.short_name")

    if has_thread:
        query.add_left_join("thread as t", "p.thread = t.id")

    if data.get("forum"):
        query.add_where_condition("p.forum = \"{}\"".format(data["forum"]))
    else:
        query.add_where_condition("p.thread = \"{}\"".format(data["thread"]))

    if "since" in data:
        query.add_more_where_condition("p.date > \"{}\"".format(data["since"]))

    query.add_order_by("p.date", data["order"])

    if "limit" in data:
        query.add_limit(data["limit"])

    return query


def get_query_list_posts_by_thread(data):
    query = Query()

    columns = "p.id, p.message, p.date, p.isApproved, p.isHighlighted, p.isEdited, p.isSpam," \
              "p.isDeleted, p.forum, p.thread, p.user, p.dislikes, p.likes, p.points, p.parent"

    query.add_select("post as p", columns)

    query.add_where_condition("p.thread = \"{}\"".format(data["thread"]))

    if "since" in data:
        query.add_more_where_condition("p.date > \"{}\"".format(data["since"]))

    query.add_order_by("p.date", data["order"])

    if "limit" in data:
        query.add_limit(data["limit"])

    return query


def get_query_remove_post_for_id(post):
    query = Query()

    query.add_update("post", " isDeleted = 1 ")
    query.add_where_condition(" id = {}".format(post))

    return query


def get_query_remove_post_for_thread(thread):
    query = Query()

    query.add_update("post", " isDeleted = 1 ")
    query.add_where_condition(" thread = {}".format(thread))

    return query


def get_query_restore_post_for_id(post):
    query = Query()

    query.add_update("post", " isDeleted = 0 ")
    query.add_where_condition(" id = {}".format(post))

    return query


def get_query_restore_post_for_thread(thread):
    query = Query()

    query.add_update("post", " isDeleted = 0 ")
    query.add_where_condition(" thread = {}".format(thread))

    return query


def get_query_update_post(post, message):
    query = Query()
    query.add_update("post", " message = \"{}\" ".format(message))
    query.add_where_condition(" id = {}".format(post))

    return query


def get_query_vote_post(post, vote):
    logger = get_logger()
    if vote == 1:
        column = "likes"
        difference = " + 1 "
    elif vote == -1:
        column = "dislikes"
        difference = " - 1 "
    else:
        return None
    logger.debug(str(post) + str(vote) + column + difference)
    query = Query()
    query.add_update("post", " {} = {} + 1, points = points {}".format(column, column, difference))
    logger.debug(query.get())
    query.add_where_condition(" id = {}".format(post))
    logger.debug(query.get())
    return query


def get_query_list_root_posts(data):
    query = Query()
    columns = "id, message, date, isApproved, isHighlighted, isEdited, isSpam,   " \
              "isDeleted, forum, thread, user, dislikes, likes,  points, parent"

    query.add_select("post", columns)

    query.add_where_condition("parent is NULL ")
    query.add_more_where_condition(" thread = {}".format(data["thread"]))

    if "since" in data:
        query.add_more_where_condition("date > \"{}\"".format(data["since"]))

    query.add_order_by("date", data["order"])

    if "limit" in data:
        query.add_limit(data["limit"])
    return query


def get_query_list_child_posts(data, id_parent, do_limit=None):
    query = Query()
    columns = "id, message, date, isApproved, isHighlighted, isEdited, isSpam,   " \
              "isDeleted, forum, thread, user, dislikes, likes,  points, parent"

    query.add_select("post", columns)

    query.add_where_condition("parent = {}".format(id_parent))

    if "since" in data:
        query.add_more_where_condition("date > \"{}\"".format(data["since"]))

    if do_limit:
        query.add_limit(data["limit"])

    query.add_order_by("date", "asc")
    return query
