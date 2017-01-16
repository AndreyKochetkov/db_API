from api_application.utils.Query import Query


def get_query_id_user_by_email(email):
    query = Query()
    query.add_select("user", ["id"])
    query.add_where_condition("email = \"{}\"".format(email))

    return query


def get_query_user_by_email(email):
    query = Query()
    query.add_select("user", ["*"])
    query.add_where_condition("email = \"{}\"".format(email))
    return query


def get_query_user_by_id(user_id):
    query = Query()
    query.add_select("user", ["*"])
    query.add_where_condition("id = \"{}\"".format(user_id))
    return query


def get_query_detail_user_by_email(email):
    query = Query()
    columns = 'u.*, group_concat(distinct f.following),' \
              'group_concat(distinct f1.follower),' \
              'group_concat(distinct s.thread)'
    query.add_select("user as u", columns)
    query.add_left_join("follow as f", "u.email = f.follower")
    query.add_left_join("follow as f1", "u.email = f1.following")
    query.add_left_join("subscribe as s", "u.email= s.user")
    query.add_where_condition("u.email = \"{}\"".format(email))
    return query


def get_query_users_by_forum(data):
    query = Query()
    columns = 'u.*, group_concat(distinct f.following),' \
              'group_concat(distinct f1.follower),' \
              'group_concat(distinct s.thread)'
    query.add_select("user as u", columns)
    query.add_left_join("follow as f", "u.email = f.follower")
    query.add_left_join("follow as f1", "u.email = f1.following")
    query.add_left_join("subscribe as s", "u.email= s.user")
    query.add_left_join("post as p", "p.user = u.email")
    query.add_where_condition("p.forum = \"{}\"".format(data["forum"]))

    if "since_id" in data:
        query.add_more_where_condition("u.id >= {}".format(data["since_id"]))

    query.add_group_by("u.id, p.user_name")
    query.add_order_by("u.name", data["order"])

    if "limit" in data:
        query.add_limit(data["limit"])
    return query


def get_query_update_user(user, about, name):
    query = Query()
    query.add_update("user", " about = \"{}\", name = \"{}\" ".format(about, name))
    query.add_where_condition(" email = \"{}\"".format(user))

    return query


def get_query_users_by_followers(data, follower=None):
    query = Query()
    columns = 'u.*, group_concat(distinct f.following),' \
              'group_concat(distinct f1.follower),' \
              'group_concat(distinct s.thread)'
    query.add_select("user as u", columns)
    query.add_left_join("follow as f", "u.email = f.follower")
    query.add_left_join("follow as f1", "u.email = f1.following")
    query.add_left_join("subscribe as s", "u.email= s.user")
    query.add_left_join("post as p", "p.user = u.email")
    if follower:
        query.add_where_condition("f.following = \"{}\"".format(data["user"]))
    else:
        query.add_where_condition("f.follower = \"{}\"".format(data["user"]))

    if "since_id" in data:
        query.add_more_where_condition(" u.id >= {}".format(data["since_id"]))
    if follower:
        query.add_group_by("f.follower")
    else:
        query.add_group_by("f.following")
    query.add_order_by("u.name", data["order"])

    if "limit" in data:
        query.add_limit(data["limit"])

    return query