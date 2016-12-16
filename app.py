import logging

from auth import register, login, whoami, logout
from flask import Flask

from flask_cors import CORS
from pymongo import MongoClient
from config import DB_NAME, MONGO_HOST, MONGO_PORT

log = logging.getLogger(__name__)
app = Flask(__name__)

CORS(app)

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT, connect=False)
db = client[DB_NAME]


app.add_url_rule('/login', view_func=login, methods=["POST"])
app.add_url_rule('/register', view_func=register, methods=["POST"])
app.add_url_rule('/whoami', view_func=whoami, methods=["GET"])
app.add_url_rule('/logout', view_func=logout, methods=["POST"])

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500