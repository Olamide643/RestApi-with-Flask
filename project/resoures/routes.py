from project.database.model import Movies
from flask import Response, request, Blueprint
import json

movies = Blueprint('movies', __name__)

@movies.route("/movies")
def get_movies():
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

@movies.route("/movies/<id>")
def get_movie(id):
    try:
        movies = Movies.objects.get(id = id).to_json()
        response = Response(movies, status = 200, mimetype='application/json')
        response.headers['Location'] = "/movie/" + str(id)
        return response

  
    except:
        error = {
            "error": "An error occured while trying to fecting data from the database"
        }
        response = Response(json.dumps(error), status=400, mimetype='application/json')
        return response

@movies.route("/movies", methods = ["POST"])
def add_movies():
    body =request.get_json()
    movie = Movies(**body)
    try:
        saved_movie = movie.save()
        id =saved_movie.id
        res = {"message": "Movie sucessfully saved", "id": str(id)}
        response = Response(json.dumps(res), status = 200, mimetype='application/json')
        response.headers['Location'] = "/movies/" + str(id)
        return response


    except:
        error = {
            "error": "An error occured while trying to insert data into the database"
        }
        response = Response(json.dumps(error), status=400, mimetype='application/json')
        return response 

@movies.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    try:
        movie_to_delete = Movies.objects.get(id = id)
        movie_to_delete.delete()
        id = movie_to_delete.id
        res = {"message": "Movie sucessfully deleted", "id": str(id)}
        response = Response(json.dumps(res), status = 200, mimetype='application/json')
        response.headers['Location'] = "/movies/delete" + str(id)
        return response
    except:
        error = {
            "error": "An error occured while trying to delete data into the database",
            "helpstring":"Kindly confirm you are passing the right id: format should be 'http://127.0.0.1:5000/movies/616c204276a0f3c468f58a88' "
        }
        response = Response(json.dumps(error), status=400, mimetype='application/json')
        response.headers['Location'] = "/movies/delete" + str(id)
        return response   


@movies.route('/movies/<id>', methods = ["PUT"])
def update_movie(id):
    try:
        movie_to_update = Movies.objects.get(id = id)
        body = request.get_json()
        movie_to_update.update(**body)
        res = {"message": "Movie sucessfully Updated", "id": str(movie_to_update.id)}
        response = Response(json.dumps(res), status = 200, mimetype='application/json')
        response.headers['Location'] = "/movies/update" + str(id)
        return response
    except:
        error = {
            "error": "An error occured while trying to update data into the database"
        }
        response = Response(json.dumps(error), status=400, mimetype='application/json')
        return response 








