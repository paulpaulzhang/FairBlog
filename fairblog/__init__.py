from os import environ

from flask import Flask
from fairblog.user_center import app_user_center
from fairblog.common import app_common
from fairblog.create import app_create
from fairblog.sign import app_sign
from fairblog.home import app_home

app = Flask(__name__)
app.register_blueprint(app_user_center)
app.register_blueprint(app_common)
app.register_blueprint(app_create)
app.register_blueprint(app_sign)
app.register_blueprint(app_home)

app.config.from_object('config')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
