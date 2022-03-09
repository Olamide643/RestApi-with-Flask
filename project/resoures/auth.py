from logging import info
from flask_jwt_extended.utils import create_access_token
from flask_restx import Resource
from mongoengine.errors import DoesNotExist, FieldDoesNotExist, NotUniqueError
from project.database.model import User
from flask import request, Response
import json, datetime
from project import api, logger
from project.error.errors import EmailAlreadyExistsError, InternalServerError, SchemaValidationError, UnauthorizededError



class Signup(Resource):
    def post(self):
        try:
            body = request.get_json()
            new_user = User(**body)
            new_user.hash_password()
            new_user.save()
            id = new_user.id
            res = { "status": "Successfully Signed Up", "userId": str(id)}
            logger.info("User {} successfully sign up with user id ".format(new_user.id))
            response = Response(json.dumps(res),status= 200, mimetype="application/json")
            response.headers["Location"] = "/User/" + str(id)
            return response

        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception as e :
            raise InternalServerError

request_schema = {
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string'
        },
        'password':{
            'type':'string'
        }
        
    }
}
request_model = api.schema_model('test_list_request', request_schema)
class LoginApi(Resource):
    @api.expect(request_model, validate=True)
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email = body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
               raise UnauthorizededError
            expires = datetime.timedelta(days= 2, seconds=50, minutes=20, hours=2)
            access_token = create_access_token(identity = str(user.id),  expires_delta=expires)
            res = {
                "message": "Succesfully Logged In",
                "token" : access_token,
                "expiresAt": "token expires at " + str(datetime.datetime.utcnow() + expires)
            }
            response = Response(json.dumps(res),200, mimetype='application/json')
            return response
        except ( UnauthorizededError, DoesNotExist):
            raise UnauthorizededError
        except Exception as e :
            raise InternalServerError
