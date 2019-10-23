import json

from flask import render_template, redirect, url_for, session, Blueprint

from fairblog import database

app_home = Blueprint('app_home', __name__, template_folder='templates')


@app_home.route('/')
def home():
    if session.get('user') is None:
        return redirect(url_for('app_sign.sign'))
    return render_template('home.html')


@app_home.route('/get-post', methods=['GET'])
def get_post():
    db = database.init()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM post ORDER BY date DESC')
    posts = list()
    for data in cursor.fetchall():
        cursor.execute('SELECT username, avatar FROM USER WHERE id = %s', data[1])
        username, avatar = cursor.fetchone()
        post = {'id': data[0],
                'uid': data[1],
                'username': username,
                'avatar': avatar,
                'content': data[2],
                'image': data[3]}
        posts.append(post)
    db.close()
    return json.dumps(posts)
