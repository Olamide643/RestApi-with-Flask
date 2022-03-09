
from flask_jwt_extended import jwt_required, get_jwt_identity
from project.database.model import Movies, User
from flask import request, Response
from flask_restx import Resource
import json
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, \
    InvalidQueryError
from project.error.errors import SchemaValidationError, MovieAlreadyExistsError, InternalServerError, \
    UpdatingMovieError,DeletingMovieError, MovieNotExistsError

class MoviesApi(Resource):
    def get(self):
        try:
            movies = Movies.objects().to_json()
            response = Response(movies, status = 200, mimetype='application/json')
            response.headers['Location'] = "/movies"
            return response
        except:
            error = {
                "error": "An error occured while trying to fecting data from the database"
            }
            response = Response(json.dumps(error), status=400, mimetype='application/json')
            return response 
    @jwt_required
    def post(self):
        
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id = user_id)
            saved_movie = Movies(**body, added_by = user).save()
            user.update(push__movies = saved_movie)
            user.save()
            id = saved_movie.id 
            res = { "status": 'movie Successfully saved', "id": str(id)}
            response = Response(json.dumps(res), status= 200, mimetype="application/json" )
            response.headers["Location"] = "/movies/" + str(id)
            return response
        except( FieldDoesNotExist,ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise MovieAlreadyExistsError
        except Exception as e:
            raise InternalServerError

class MovieApi(Resource):
    def get(self, id):
        try:
            movies = Movies.objects.get(id = id).to_json()
            response = Response(movies, status = 200, mimetype='application/json')
            response.headers['Location'] = "/movie/" + str(id)
            return response

        except DoesNotExist:
            raise MovieNotExistsError
        except Exception:
            raise InternalServerError

    @jwt_required
    def delete(self,id):
        user_id = get_jwt_identity()
        try:
            movie_to_delete = Movies.objects.get(id = id, added_by = user_id)
            movie_to_delete.delete()
            id = movie_to_delete.id
            res = {"message": "Movie sucessfully deleted", "id": str(id)}
            response = Response(json.dumps(res), status = 200, mimetype='application/json')
            response.headers['Location'] = "/movies/delete" + str(id)
            return response
        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError
    @jwt_required
    def put(self,id):
        user_id = get_jwt_identity()
        try:
            user = User.objects.get(id = user_id)
            movie_to_update = Movies.objects.get(id = id, added_by = user)
            body = request.get_json()
            movie_to_update.update(**body)
            res = {"message": "Movie sucessfully Updated", "id": str(movie_to_update.id)}
            response = Response(json.dumps(res), status = 200, mimetype='application/json')
            response.headers['Location'] = "/movies/update" + str(id)
            return response
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingMovieError

        except Exception:
            raise InternalServerError


