from config import Config
from flask import Flask, render_template

app = Flask(__name__)

app.config.from_object(Config)

from flask_login import LoginManager

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
login_manager.login_message = "You cannot access this page"

from app import routes


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
