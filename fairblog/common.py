import json

from flask import render_template, session, Blueprint

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
    cursor.execute('SELECT id, avatar FROM user WHERE username=%s', username)
    uid, avatar = cursor.fetchone()
    db.close()
    res = {'username': username, 'uid': uid, 'avatar': avatar}
    return json.dumps(res)
