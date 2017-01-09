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
    columns = 'u.*, group_concat(distinct f.following) as following,' \
              'group_concat(distinct f1.follower) as followers,' \
              'group_concat(distinct s.thread) as subscriptions'
    query.add_select("user as u", columns)
    query.add_left_join("follow as f", "u.email = f.follower")
    query.add_left_join("follow as f1", "u.email = f1.following")
    query.add_left_join("subscribe as s", "u.email= s.user")
    query.add_where_condition("u.email = \"{}\"".format(email))
    return query
