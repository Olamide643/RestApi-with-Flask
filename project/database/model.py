from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class Movies(db.Document):
    name = db.StringField(required = True, unique = True)
    casts = db.ListField(db.StringField(),required = True)
    genres = db.ListField(db.StringField(),required = True)
    added_by = db.ReferenceField('User')


class User(db.Document):
    email = db.EmailField(required = True, unique = True)
    password = db.StringField(required = True)
    # removes a movie from the user when  a movie is deleted 
    movies = db.ListField(db.ReferenceField('Movies', reverse_delete_rule = db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    def check_password(self,password):
        return check_password_hash(self.password,password)

# removes all movies created by a user when the user is deleted 
User.register_delete_rule(Movies, 'added_by', db.CASCADE)





