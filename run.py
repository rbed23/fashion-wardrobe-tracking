from logging.config import dictConfig
from logging import getLogger

from fashion_wardrobe_tracker import app, db
from fashion_wardrobe_tracker.logger import ROOT_LOGGER_CONFIG


if __name__ == "__main__":

    dictConfig(ROOT_LOGGER_CONFIG)  # modify werkzeug logs
    db.create_all(app=app)          # create tables from models
    
    app.run()                       # start
