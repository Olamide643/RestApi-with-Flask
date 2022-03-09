from flask import render_template, request
from project.database.model import User
from flask_restful import Resource
from datetime import datetime
from flask_jwt_extended import create_access_token, decode_token

from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError
from project.error.errors import BadTokenError, EmailDoesnotExistsError, SchemaValidationError, InternalServerError, ExpiredTokenError
from .mail_services import send_mail


class ForgetPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            email = body.get('email')
            if not email:
                raise SchemaValidationError
            user = User.objects.get(email = email)
            if not user:
                raise EmailDoesnotExistsError
            expires = datetime.timdelta(minutes = 10)
            reset_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return send_mail(subject="[Movie-Collection] Reset your Password",
                sender='noreply@moviecollectionSupport.com', 
                recipients=[user.email], 
                text_body= render_template('mail/reset_password.txt',url = url +reset_token),
                html_body= render_template('mail/resest_password.html', url = url + reset_token)
                )
            
        except SchemaValidationError:
            raise SchemaValidationError
        except EmailDoesnotExistsError:
            raise EmailDoesnotExistsError
        except Exception as e:
            raise InternalServerError



class ResetPassword(Resource):
    def post(self):
        try:
            body = request.get_json()
            reset_token = body.get("reset_token")
            password = body.get("password")

            if not reset_token or password:
                raise SchemaValidationError
            user_id = decode_token(reset_token)['identity']
            user = User.objects.get(id = user_id)
            user.modify(password = password)
            user.hash_password()
            user.save()

            return send_mail(
                  subject="[Movie-Collection] Password Reset Successfully",
                  sender= 'noreply@moviecollectionsupport.com',
                  recipients= [user.email],
                  text_body= render_template("Password was Reset Successfully"),
                  html_body= "<p> Password was Reset Successfully </p>"
            )
        except SchemaValidationError:
            raise SchemaValidationError
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except (DecodeError, InvalidTokenError):
            raise  BadTokenError
        except Exception as e:
            raise InternalServerError
