from api_application.utils.Query import Query


def get_query_post_by_id(post_id):
    query = Query()
    query.add_select("post", ["id"])
    query.add_where_condition("id = \"{}\"".format(post_id))
    return query


def get_query_detail_post_by_id(id_post, has_forum, has_thread):
    query = Query()

    columns = 'p.id, p.message, p.date, p.isApproved, p.isHighlighted, p.isEdited, p.isSpam, ' \
              'p.isDeleted, p.forum, p.thread, p.user, p.dislikes, p.likes, p.points, p.parent'
    if has_forum:
        columns += ", f.name f_name, f.short_name f_short_name, f.user f_user, f.id f_id"

    if has_thread:
        columns += ', t.id t_id, t.forum t_forum, t.title t_title, t.isClosed t_isClosed, ' \
                   't.user t_user, t.date t_date, t.message t_message, t.slug t_slug, t.isDeleted t_isDeleted, ' \
                   't.posts t_posts, t.likes t_likes, t.dislikes t_dislikes, t.points t_points'

    query.add_select("post as p", columns)

    if has_forum:
        query.add_left_join("forum as f", "p.forum = f.short_name")

    if has_thread:
        query.add_left_join("thread as t", "p.thread = t.id")
    query.add_where_condition("p.id = \"{}\"".format(id_post))

    return query
