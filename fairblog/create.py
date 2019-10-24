import re
import time

from flask import render_template, request, session, redirect, url_for, Blueprint

from fairblog import database, tool

app_create = Blueprint('app_create', __name__, template_folder='templates')


@app_create.route('/create')
def create():
    if session.get('user') is None:
        return redirect(url_for('sign'))
    return render_template('create.html')


@app_create.route('/create-post', methods=['POST'])
def create_post():
    uid = request.form['uid']
    text = request.form['text']
    image64 = request.form['image']
    img_info = re.search('data:image/(?P<ext>.*?);base64,(?P<data>.*)', image64, re.DOTALL)

    if img_info:
        res_path = tool.save_base64_img(img_info)
        db = database.init()
        cursor = db.cursor()
        cursor.execute('INSERT INTO post(uid, content, image, date) VALUES(%s, %s, %s, %s)',
                       (int(uid), text, res_path, int(round(time.time() * 1000))))
        db.commit()
        db.close()
        return 'ok'
    else:
        raise Exception('Cannot parse!')
