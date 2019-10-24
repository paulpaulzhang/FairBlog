import json

from flask import render_template, session, Blueprint, request

from fairblog import database

app_common = Blueprint('app_common', __name__, template_folder='templates')


@app_common.route('/test', methods=['POST', 'GET'])
def test():
    return render_template('test.html')


@app_common.route('/get-user', methods=['GET'])
def get_user():
    username = session.get('user')
    db = database.init()
    cursor = db.cursor()
    cursor.execute('SELECT id, avatar, gender, introduction FROM user WHERE username=%s', username)
    uid, avatar, gender, introduction = cursor.fetchone()
    db.close()
    res = {
        'username': username,
        'uid': uid,
        'avatar': avatar,
        'gender': gender,
        'introduction': introduction
    }
    return json.dumps(res)


@app_common.route('/get-user-by-uid', methods=['GET', 'POST'])
def get_user_by_uid():
    uid = request.form['uid']
    db = database.init()
    cursor = db.cursor()
    cursor.execute('SELECT username, avatar, gender, introduction FROM user WHERE id=%s', uid)
    username, avatar, gender, introduction = cursor.fetchone()
    db.close()
    res = {
        'username': username,
        'uid': uid,
        'avatar': avatar,
        'gender': gender,
        'introduction': introduction
    }
    return json.dumps(res)
