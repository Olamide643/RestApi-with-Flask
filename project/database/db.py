from flask_mongoengine import MongoEngine
db = MongoEngine()

def Initialize_db(app):
    db.init_app(app)
 