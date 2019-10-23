import base64
import re
import uuid
import config
import time

from flask import render_template, request, session, redirect, url_for, Blueprint

from fairblog import database

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
        ext = img_info.groupdict().get('ext')  # 后缀
        data = img_info.groupdict().get('data')  # 图片data

        image = base64.urlsafe_b64decode(data)
        filename = "{}.{}".format(uuid.uuid4(), ext)  # 文件名
        path = "{}{}".format(config.IMAGE_PATH, filename)  # 服务器图片存路径
        with open(path, mode='wb') as f:
            f.write(image)
        res_path = '{}{}'.format(config.FTP_HOST, filename)
        db = database.init()
        cursor = db.cursor()
        cursor.execute('INSERT INTO post(uid, content, image, date) VALUES(%s, %s, %s, %s)',
                       (int(uid), text, res_path, int(round(time.time() * 1000))))
        db.commit()
        db.close()
        return 'ok'
    else:
        raise Exception('Cannot parse!')
