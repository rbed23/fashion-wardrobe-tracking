from logging import getLogger, NullHandler
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask.logging import default_handler
from flask_migrate import Migrate

from .auth import login_manager
from .data import db
import fashion_wardrobe_tracker.errors as errors
import fashion_wardrobe_tracker.logger as logger
from .tracking.views import tracking
from .users.views import users


# load .env variables
load_dotenv('.env')


# setup custom logger
getLogger(__name__).addHandler(NullHandler())

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# make init calls to setup app
db.init_app(app)
login_manager.init_app(app)
errors.init_app(app)
logger.init_app(app, app.logger.level) if\
    app.logger.level != 0 else\
    logger.init_app(app, app.logger.parent.level)


app.register_blueprint(tracking)
app.register_blueprint(users)


@app.before_request
def log_it():
    app.logger.info("Handling Request")


@app.context_processor
def provide_constants():
    return {"constants": {"TUTORIAL_PART": 2}}
