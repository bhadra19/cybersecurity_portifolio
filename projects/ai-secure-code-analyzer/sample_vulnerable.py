def find_user(db, username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return db.execute(query)


def render_comment(comment):
    return "<div>" + comment + "</div>"
