from flask import render_template, request, session, Blueprint

from fairblog import database

app_sign = Blueprint('app_sign', __name__, template_folder='templates')


@app_sign.route('/sign', methods=['GET'])
def sign():
    return render_template('sign.html')


@app_sign.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    db = database.init()
    cursor = db.cursor()
    cursor.execute('SELECT username FROM user WHERE username= %s', username)
    username_ = cursor.fetchone()
    if username_:
        cursor.execute('SELECT password FROM user WHERE username= %s', username)
        password_ = cursor.fetchone()[0]
        if password == password_:
            session['user'] = username
            return 'ok'
        else:
            return '用户名或密码错误'
    else:
        return '用户名不存在'


@app_sign.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    db = database.init()
    cursor = db.cursor()
    cursor.execute('SELECT username FROM user WHERE username = %s', username)
    username_ = cursor.fetchone()
    if not username_:
        cursor.execute('INSERT INTO user(username, password, avatar) VALUES(%s, %s, %s)',
                       (username, password, 'http://188.131.253.83:8092/img/default/avatar.png'))
        db.commit()
        db.close()
        session['user'] = username
        return 'ok'
    else:
        db.close()
        return '用户名已存在'
