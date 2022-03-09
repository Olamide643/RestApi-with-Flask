import logging
from flask import Flask
from project.database.db import Initialize_db
import os
from logging.handlers import TimedRotatingFileHandler
import logging 
from werkzeug.utils import cached_property


from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from project.error.errors import errors
from flask_mail import Mail

def Logger():
    logger = logging.getLogger(name = "logs")
    #logname = os.path.join(os.getcwd(),"project","logs","log.txt")
    logname = 'project\logs\logfile.txt'
    formater = logging.Formatter(
        '[%(asctime)s:%(levelname)s]  %(message)s'
    )
    error_handler = TimedRotatingFileHandler(logname, when='midnight', interval=1)
    error_handler.suffix = "%Y-%m-%d"
    error_handler.setLevel(logging.DEBUG)
    error_handler.setFormatter(formater)
    logger.addHandler(error_handler)
    return logger 

logger = Logger()
    


app = Flask(__name__)
#app.config.from_envvar('ENV_FILE_ENV')
mail = Mail(app)
api = Api(app, errors=errors)
from project.resoures.initialize_routes import initialize_routes

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

logger = Logger()
Initialize_db(app)
initialize_routes(api)
#app.register_blueprint(movies) // Uncomment for function defined url



