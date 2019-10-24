import json
import re

from flask import render_template, request, session, redirect, url_for, Blueprint

from fairblog import database, tool

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


@app_user_center.route('/update-user-info', methods=['GET', 'POST'])
def update_username_info():
    uid = request.form['uid']
    username = request.form['username']
    gender = request.form['gender']
    introduction = request.form['introduction']

    db = database.init()
    cursor = db.cursor()
    cursor.execute("UPDATE user SET username = %s, gender = %s, introduction = %s WHERE id = %s",
                   (username, gender, introduction, uid))
    db.commit()
    db.close()
    return 'ok'


@app_user_center.route('/update-password', methods=['GET', 'POST'])
def update_password():
    uid = request.form['uid']
    password = request.form['password']

    db = database.init()
    cursor = db.cursor()
    cursor.execute('UPDATE user SET password = %s WHERE id = %s', (password, uid))
    db.commit()
    db.close()
    return 'ok'


@app_user_center.route('/update-avatar', methods=['GET', 'POST'])
def update_avatar():
    uid = request.form['uid']
    image64 = request.form['avatar']
    img_info = re.search('data:image/(?P<ext>.*?);base64,(?P<data>.*)', image64, re.DOTALL)
    if img_info:
        res_path = tool.save_base64_img(img_info)
        db = database.init()
        cursor = db.cursor()
        cursor.execute('UPDATE user SET avatar = %s WHERE id = %s', (res_path, uid))
        db.commit()
        db.close()
    return 'ok'


@app_user_center.route('/logout', methods=['POST'])
def logout():
    session['user'] = None
    return 'ok'
