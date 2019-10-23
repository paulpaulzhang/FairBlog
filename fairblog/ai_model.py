import json

from flask import render_template, request, session, redirect, url_for, Blueprint

app_ai = Blueprint('app_ai', __name__, template_folder='templates')


@app_ai.route('/ai')
def ai():
    return render_template('ai.html')


@app_ai.route('/ai-init')
def init():
    return 'ok'


@app_ai.route('/ai-test')
def test_model():
    return 'test'
