from pymysql import connect

HOST = '188.131.253.83'
USERNAME = 'root'
PASSWORD = 'ZLM0315zlm'
DATABASE = 'fairblog'


def init():
    return connect(HOST, USERNAME, PASSWORD, DATABASE)
