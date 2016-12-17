import logging
from flask import Flask
from flask_cors import CORS
from api.listings import ListingsView
from api.auth import register, login, whoami, logout

log = logging.getLogger(__name__)
app = Flask(__name__)

CORS(app)

app.add_url_rule('/login', view_func=login, methods=["POST"])
app.add_url_rule('/register', view_func=register, methods=["POST"])
app.add_url_rule('/whoami', view_func=whoami, methods=["GET"])
app.add_url_rule('/logout', view_func=logout, methods=["POST"])
app.add_url_rule('/listings', view_func=ListingsView.as_view(name="listings"))

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

app.run()