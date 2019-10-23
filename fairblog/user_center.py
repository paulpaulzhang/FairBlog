import json

from flask import render_template, request, session, redirect, url_for, Blueprint

from fairblog import database

app_user_center = Blueprint('app_user_center', __name__, template_folder='templates')


@app_user_center.route('/user-center')
def user_center():
    if session.get('user') is None:
        return redirect(url_for('sign'))
    return render_template('user_center.html')


@app_user_center.route('/get-post-by-uid', methods=['GET', 'POST'])
def get_post_by_uid():
    uid = request.form['uid']
    db = database.init()
    cursor = db.cursor()
    cursor.execute('SELECT id, content, image FROM post WHERE uid = %s ORDER BY date DESC', uid)
    posts = list()
    for data in cursor.fetchall():
        post = {
            'pid': data[0],
            'content': data[1],
            'image': data[2]
        }
        posts.append(post)
    return json.dumps(posts)
